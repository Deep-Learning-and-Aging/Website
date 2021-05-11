from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items
from dash_website.utils.graphs import (
    heatmap_by_clustering,
    heatmap_by_sorted_dimensions,
    add_custom_legend_axis,
    histogram_correlation,
)
from dash_website import DOWNLOAD_CONFIG, ORDER_TYPES, CUSTOM_ORDER, ORDER_DIMENSIONS
from dash_website.correlation_between import SAMPLE_DEFINITION


def get_custom_dimensions():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_custom_dimensions")),
            html.H1("Correlation between accelerated aging dimensions"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_custom_dimensions(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_custom_dimensions"),
                                    dcc.Graph(id="graph_custom_dimensions", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 9},
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H4("Histogram of the above correlations"),
                                    dcc.Graph(id="histogram_custom_dimensions", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 6, "offset": 3},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


@APP.callback(
    Output("memory_custom_dimensions", "data"),
    Input("sample_definition_custom_dimensions", "value"),
)
def _modify_store_custom_dimensions(sample_definition):
    return load_feather(
        f"correlation_between_accelerated_aging_dimensions/custom_dimensions_{sample_definition}.feather"
    ).to_dict()


def get_controls_tab_custom_dimensions():
    return dbc.Card(
        [
            get_item_radio_items(
                "sample_definition_custom_dimensions", SAMPLE_DEFINITION, "Select the way we define a sample: "
            ),
            get_item_radio_items("order_type_custom_dimensions", ORDER_TYPES, "Order by:"),
        ]
    )


@APP.callback(
    [
        Output("graph_custom_dimensions", "figure"),
        Output("title_custom_dimensions", "children"),
        Output("histogram_custom_dimensions", "figure"),
    ],
    [
        Input("order_type_custom_dimensions", "value"),
        Input("memory_custom_dimensions", "data"),
    ],
)
def _fill_graph_tab_custom_dimensions(order_by, data_custom_dimensions):
    correlations = pd.DataFrame(data_custom_dimensions)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]

    customdata_list = []
    for customdata_item in ["correlation_std", "r2_1", "r2_std_1", "r2_2", "r2_std_2"]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            )
            .loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]
            .values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=ORDER_DIMENSIONS, columns=ORDER_DIMENSIONS)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>r2: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>Dimensions 2: %{y} <br>r2: %{customdata[3]:.3f} +- %{customdata[4]:.3f}<br><extra></extra>"

    if order_by == "clustering":
        fig = heatmap_by_clustering(table_correlations, hovertemplate, customdata)
    elif order_by == "r2":
        sorted_dimensions = (
            correlations.set_index(["dimension_1", "subdimension_1"])
            .sort_values(by="r2_1", ascending=False)
            .index.drop_duplicates()
        )

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

    else:  # order_by == "custom"
        sorted_dimensions = (
            correlations.set_index(["dimension_1", "subdimension_1"]).loc[CUSTOM_ORDER].index.drop_duplicates()
        )

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

        fig = add_custom_legend_axis(fig, sorted_table_correlations)

    if order_by != "custom":
        fig.update_layout(font={"size": 8})

    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False},
        xaxis={"showgrid": False, "zeroline": False},
        width=1100,
        height=1100,
    )

    return (
        fig,
        f"Average correlation = {correlations['correlation'].mean().round(3)} +- {correlations['correlation'].std().round(3)}",
        histogram_correlation(table_correlations),
    )
