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


def get_data():
    return load_feather("genetics/correlations/correlations.feather").to_dict()


def get_controls_genetics_correlations():
    return dbc.Card(get_item_radio_items("order_type_genetics_correlations", ORDER_TYPES, "Order by:"))


@APP.callback(
    [
        Output("graph_genetics_correlations", "figure"),
        Output("title_genetics_correlations", "children"),
        Output("histogram_correlations", "figure"),
    ],
    [
        Input("order_type_genetics_correlations", "value"),
        Input("memory_genetics_correlations", "data"),
    ],
)
def _fill_graph_genetics_correlations(order_by, data_genetics_correlations):
    correlations = pd.DataFrame(data_genetics_correlations)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[ORDER_DIMENSIONS.drop(("Eyes", "All")), ORDER_DIMENSIONS.drop(("Eyes", "All"))]
    np.fill_diagonal(table_correlations.values, np.nan)

    customdata_list = []
    for customdata_item in [
        "correlation_std",
        "r2_1",
        "r2_std_1",
        "h2_1",
        "h2_std_1",
        "r2_2",
        "r2_std_2",
        "h2_2",
        "h2_std_2",
    ]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            )
            .loc[ORDER_DIMENSIONS.drop(("Eyes", "All")), ORDER_DIMENSIONS.drop(("Eyes", "All"))]
            .values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(
        None, index=ORDER_DIMENSIONS.drop(("Eyes", "All")), columns=ORDER_DIMENSIONS.drop(("Eyes", "All"))
    )
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>R2: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>h²: %{customdata[3]:.3f} +- %{customdata[4]:.3f} <br>Dimensions 2: %{y}<br>R2: %{customdata[5]:.3f} +- %{customdata[6]:.3f}<br>h²: %{customdata[7]:.3f} +- %{customdata[8]:.3f}<br><extra></extra>"

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


LAYOUT = dbc.Container(
    [
        dcc.Loading(dcc.Store(id="memory_genetics_correlations", data=get_data())),
        html.H1("Genetics - Correlations"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_controls_genetics_correlations(),
                        html.Br(),
                        html.Br(),
                    ],
                    width={"size": 3},
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H2(id="title_genetics_correlations"),
                                dcc.Graph(id="graph_genetics_correlations", config=DOWNLOAD_CONFIG),
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
                                dcc.Graph(id="histogram_correlations", config=DOWNLOAD_CONFIG),
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
