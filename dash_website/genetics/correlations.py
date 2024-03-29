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
from dash_website import CUSTOM_DIMENSIONS, ORDER_TYPES, GRAPH_SIZE, DOWNLOAD_CONFIG, DIMENSIONS_SUBDIMENSIONS_INDEXES
from dash_website.genetics import DIMENSIONS_TO_DROP_CORRELATIONS


def get_controls_genetics_correlations():
    return dbc.Card(get_item_radio_items("order_type_genetics_correlations", ORDER_TYPES, "Order by:"))


@APP.callback(
    [
        Output("graph_genetics_correlations", "figure"),
        Output("title_genetics_correlations", "children"),
        Output("histogram_genetics_correlations", "figure"),
    ],
    [
        Input("order_type_genetics_correlations", "value"),
        Input("memory_genetics_correlations", "data"),
        Input("memory_scores_genetics_correlations", "data"),
        Input("memory_heritability_genetics_correlations", "data"),
    ],
)
def _fill_graph_genetics_correlations(order_by, data_genetics_correlations, data_scores, data_heritability):
    correlations = pd.DataFrame(data_genetics_correlations)

    scores = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"])
    scores.drop(index=scores.index[~scores.index.isin(CUSTOM_DIMENSIONS)], inplace=True)
    scores.reset_index(["sub_subdimension", "algorithm"], drop=True, inplace=True)

    heritabilities = pd.DataFrame(data_heritability).set_index(["dimension", "subdimension"])

    for number in [1, 2]:
        correlations.set_index([f"dimension_{number}", f"subdimension_{number}"], inplace=True)
        correlations[f"r2_{number}"] = scores["r2"]
        correlations[f"r2_std_{number}"] = scores["r2_std"]
        correlations[f"h2_{number}"] = heritabilities["h2"]
        correlations[f"h2_std_{number}"] = heritabilities["h2_std"]
        correlations.reset_index(inplace=True)

    custom_dimensions = DIMENSIONS_SUBDIMENSIONS_INDEXES.drop(DIMENSIONS_TO_DROP_CORRELATIONS)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[custom_dimensions, custom_dimensions]
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
        customdata_value = (
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            )
            .loc[custom_dimensions, custom_dimensions]
            .values
        )

        if customdata_item == "correlation_std":
            np.fill_diagonal(customdata_value, np.nan)

        customdata_list.append(customdata_value)
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=custom_dimensions, columns=custom_dimensions)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>h²: %{customdata[3]:.3f} +- %{customdata[4]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[5]:.3f} +- %{customdata[6]:.3f}<br>h²: %{customdata[7]:.3f} +- %{customdata[8]:.3f}<br><extra></extra>"

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
        fig = heatmap_by_sorted_dimensions(table_correlations, hovertemplate, customdata)
        fig = add_custom_legend_axis(fig, table_correlations.index)
        fig = add_custom_legend_axis(fig, table_correlations.index, horizontal=False)

    if order_by != "custom":
        fig.update_layout(font={"size": 8})

    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False},
        xaxis={"showgrid": False, "zeroline": False},
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return (
        fig,
        f"Average correlation = {correlations['correlation'].mean().round(3)} +- {correlations['correlation'].std().round(3)}",
        histogram_correlation(table_correlations),
    )


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(
                    id="memory_genetics_correlations",
                    data=load_feather("genetics/correlations/correlations.feather").to_dict(),
                ),
                dcc.Store(
                    id="memory_scores_genetics_correlations",
                    data=load_feather(
                        "age_prediction_performances/scores_all_samples_per_participant.feather"
                    ).to_dict(),
                ),
                dcc.Store(
                    id="memory_heritability_genetics_correlations",
                    data=load_feather(f"genetics/heritability/heritability.feather").to_dict(),
                ),
            ]
        ),
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
                                dcc.Graph(id="histogram_genetics_correlations", config=DOWNLOAD_CONFIG),
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
