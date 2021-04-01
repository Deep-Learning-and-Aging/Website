from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.controls import (
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
    get_dimension_drop_down,
)
from dash_website import DIMENSIONS


def get_average_bars():
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [
                            html.H2(id="title_average_test"),
                            dcc.Graph(id="graph_average"),
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab():
    return dbc.Card(
        [
            get_dimension_drop_down(
                "dimension_1_average", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_dimension=1
            ),
            html.Div(
                [get_dimension_drop_down("dimension_2_average", ["average"] + DIMENSIONS, idx_dimension=2)],
                id="hiden_dimension_2_average",
                style={"display": "none"},
            ),
            get_subset_method_radio_items("subset_method_correlations"),
            get_correlation_type_radio_items("correlation_type_average"),
        ]
    )


@APP.callback(
    [
        Output("hiden_dimension_2_average", component_property="style"),
        Output("dimension_2_average", "options"),
        Output("dimension_2_average", "value"),
    ],
    Input("dimension_1_average", "value"),
)
def _change_controls_average(dimension_1):
    if dimension_1 in ["MainDimensions", "SubDimensions"]:
        return {"display": "none"}, get_options(["average"]), "average"
    else:
        return (
            {"display": "block"},
            get_options(["average"] + pd.Index(DIMENSIONS).drop(dimension_1).tolist()),
            "average",
        )


@APP.callback(
    [Output("graph_average", "figure"), Output("title_average_test", "children")],
    [
        Input("correlation_type_average", "value"),
        Input("dimension_1_average", "value"),
        Input("dimension_2_average", "value"),
        Input("memory_correlations", "data"),
    ],
)
def _fill_graph_tab_average(correlation_type, dimension_1, dimension_2, data):
    import plotly.graph_objs as go

    correlations = pd.DataFrame(data).set_index(["dimension_1", "dimension_2", "category"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["subset_method", "observation"]
    )

    if (
        dimension_1 in ["MainDimensions", "SubDimensions"]
        or dimension_2 == "average"
        or np.nonzero(np.array(DIMENSIONS) == dimension_1)[0][0] < np.nonzero(np.array(DIMENSIONS) == dimension_2)[0][0]
    ):
        sorted_correlations = correlations.loc[(dimension_1, dimension_2), correlation_type].sort_values(
            by=["mean"], ascending=False
        )
    else:
        sorted_correlations = (
            correlations.swaplevel(i=0, j=1)
            .loc[(dimension_1, dimension_2), correlation_type]
            .sort_values(by=["mean"], ascending=False)
        )

    bars = go.Bar(
        x=sorted_correlations.index,
        y=sorted_correlations["mean"],
        error_y={"array": sorted_correlations["std"], "type": "data"},
        name="Average correlations",
        marker_color="indianred",
    )

    fig = go.Figure(bars)
    fig.update_layout(
        {
            "width": 1500,
            "height": 500,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
        }
    )

    return fig, f"{dimension_1}_{dimension_2}"
