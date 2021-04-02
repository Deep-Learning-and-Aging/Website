from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_dimension_drop_down, get_options
from dash_website import DIMENSIONS, RENAME_DIMENSIONS


def get_average_bars(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dcc.Loading([dcc.Store(id="memory_averages", data=get_data())]),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_average(subset_method_radio_items, correlation_type_radio_items),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_average_test"),
                                    dcc.Graph(id="graph_average"),
                                ]
                            )
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
    return load_feather(f"xwas/univariate_correlations/averages_correlations.feather").to_dict()


def get_controls_tab_average(subset_method_radio_items, correlation_type_radio_items):
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
            subset_method_radio_items,
            correlation_type_radio_items,
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
        Input("subset_method_correlations", "value"),
        Input("correlation_type_correlations", "value"),
        Input("dimension_1_average", "value"),
        Input("dimension_2_average", "value"),
        Input("memory_correlations", "data"),
        Input("memory_averages", "data"),
    ],
)
def _fill_graph_tab_average(
    subset_method, correlation_type, dimension_1, dimension_2, data_correlations, data_averages
):
    import plotly.graph_objs as go

    if dimension_2 == "average":
        averages = pd.DataFrame(data_averages).set_index(["dimension", "category"])
        averages.columns = pd.MultiIndex.from_tuples(
            list(map(eval, averages.columns.tolist())), names=["subset_method", "correlation_type", "observation"]
        )

        sorted_averages = averages.loc[dimension_1, (subset_method, correlation_type)].sort_values(
            by=["mean"], ascending=False
        )

        bars = go.Bar(
            x=sorted_averages.index,
            y=sorted_averages["mean"],
            error_y={"array": sorted_averages["std"], "type": "data"},
            name="Average correlations",
            marker_color="indianred",
        )

        title = f"Average average correlation across aging dimensions and X categories = {sorted_averages['mean'].mean().round(3)} +- {sorted_averages['mean'].std().round(3)}"
        y_label = "Average correlation"

    else:
        correlations = pd.DataFrame(data_correlations).set_index(["dimension_1", "dimension_2", "category"])

        sorted_correlations = correlations.loc[(dimension_1, dimension_2)].sort_values(
            by=["correlation"], ascending=False
        )

        bars = go.Bar(
            x=sorted_correlations.index,
            y=sorted_correlations["correlation"],
            name="Correlations",
            marker_color="indianred",
        )

        title = f"Average correlation = {sorted_correlations['correlation'].mean().round(3)} +- {sorted_correlations['correlation'].std().round(3)}"
        y_label = "Correlation"

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 1500,
            "height": 500,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": y_label},
        }
    )

    return fig, title
