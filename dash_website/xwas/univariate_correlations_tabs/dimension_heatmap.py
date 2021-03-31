from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_dimension_drop_down,
)
from dash_website.utils.aws_loader import load_feather
from dash_website import DIMENSIONS


def get_dimension_heatmap():
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dcc.Store(id="memory_dimension", data=get_data()),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [
                            html.H2(id="title_dimension"),
                            dcc.Graph(id="graph_dimension"),
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather(f"xwas/univariate_correlations/correlations.feather").to_dict()


def get_controls_tab():
    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension", DIMENSIONS),
            get_subset_method_radio_items("subset_method_dimension"),
            get_correlation_type_radio_items("correlation_type_dimension"),
        ]
    )


@APP.callback(
    [Output("graph_dimension", "figure"), Output("title_dimension", "children")],
    [
        Input("dimension_dimension", "value"),
        Input("subset_method_dimension", "value"),
        Input("correlation_type_dimension", "value"),
        Input("memory_dimension", "data"),
    ],
)
def _fill_graph_tab_organ(dimension, subset_method, correlation_type, data):
    from dash_website.utils.graphs.colorscale import get_colorscale
    import plotly.graph_objs as go

    correlations = pd.DataFrame(data).set_index(["dimension_1", "dimension_2", "category"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["category", "variable"]
    )
    matrix_correlations_2d = correlations[(subset_method, correlation_type)].swaplevel().loc[dimension]
    matrix_correlations_2d.name = "correlation"
    correlations_2d = pd.pivot_table(
        matrix_correlations_2d.to_frame(), values="correlation", index="dimension_2", columns="category"
    )

    matrix_number_variables_2d = correlations[(subset_method, "number_variables")].swaplevel().loc[dimension]
    matrix_number_variables_2d.name = "number_variables"
    number_variables_2d = pd.pivot_table(
        matrix_number_variables_2d.to_frame(), values="number_variables", index="dimension_2", columns="category"
    )

    hovertemplate = "Correlation: %{z:.3f} <br>X subcategory: %{x} <br>Aging dimension: %{y} <br>Number variables: %{customdata} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=correlations_2d.columns,
        y=correlations_2d.index,
        z=correlations_2d,
        colorscale=get_colorscale(correlations_2d),
        customdata=number_variables_2d,
        hovertemplate=hovertemplate,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        {
            "width": 2000,
            "height": 1000,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "Aging dimension", "showgrid": False},
        }
    )

    return fig, "Average correlation = ??? ± ???"