from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
    get_dimension_drop_down,
)
from dash_website.utils.aws_loader import load_csv, load_excel
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES


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
                            dcc.Loading(
                                [
                                    html.H2(id="scores_average"),
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


def get_controls_tab():
    return dbc.Card(
        [
            get_dimension_drop_down(
                "dimension_1_average", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_dimension=1
            ),
            html.Div(
                [get_dimension_drop_down("dimension_2_average", ["Average"] + DIMENSIONS, idx_dimension=2)],
                id="hiden_dimension_2_average",
                style={"display": "block"},
            ),
            get_subset_method_radio_items("subset_method_average"),
            get_correlation_type_radio_items("correlation_type_average"),
        ]
    )


@APP.callback(
    [Output("graph_average", "figure"), Output("scores_average", "children")],
    [
        Input("correlation_type_average", "value"),
        Input("subset_method_average", "value"),
        Input("organs_organ_1", "value"),
        Input("organs_organ_2", "value"),
    ],
)
def _fill_graph_tab_average(correlation_type, subset_method, organ_1, organ_2):
    from plotly.graph_objs import Figure
    from dash_website.utils.graphs.bar import create_bar

    correlations_mean = load_excel(
        f"page6_LinearXWASCorrelations/average_correlations/Correlations_comparisons_{subset_method}_{correlation_type}.xlsx",
        index_col=[0, 1],
    ).loc[(organ_1, organ_2)]
    correlations_std = load_excel(
        f"page6_LinearXWASCorrelations/average_correlations/Correlations_sd_comparisons_{subset_method}_{correlation_type}.xlsx",
        index_col=[0, 1],
    ).loc[(organ_1, organ_2)]

    fig = Figure()
    fig.add_trace(create_bar(correlations_mean, correlations_std))
    fig.update_layout(xaxis_tickangle=-90)
    fig.update_layout({"width": 1800, "height": 600})

    return fig, f"{organ_1}_{organ_2}"
