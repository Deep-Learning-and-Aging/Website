from dash_website.app import APP
import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items, get_options_from_list
from dash_website.utils.graphs import (
    heatmap_by_clustering,
    heatmap_by_sorted_dimensions,
    add_custom_legend_axis,
    histogram_correlation,
)
from dash_website import (
    DOWNLOAD_CONFIG,
    MAIN_CATEGORIES_TO_CATEGORIES,
    ALGORITHMS,
    CORRELATION_TYPES,
    CUSTOM_DIMENSIONS,
    ORDER_TYPES,
    GRAPH_SIZE,
    DIMENSIONS_SUBDIMENSIONS_INDEXES,
)
from dash_website.xwas import MULTIVARIATE_CATEGORIES_TO_REMOVE


def get_heatmap_multivariate_category():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(id="memory_category_multivariate"),
                    dcc.Store(
                        id="memory_scores_category_multivariate",
                        data=load_feather(
                            "age_prediction_performances/scores_all_samples_per_participant.feather"
                        ).to_dict(),
                    ),
                ]
            ),
            html.H1("Multivariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_category_multivariate(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_category_multivariate"),
                                    dcc.Graph(id="graph_category_multivariate", config=DOWNLOAD_CONFIG),
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
                                    dcc.Graph(id="histogram_category_multivariate", config=DOWNLOAD_CONFIG),
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


@APP.callback(Output("memory_category_multivariate", "data"), Input("category_category_multivariate", "value"))
def _modify_store_category_multivariate(category):
    return load_feather(
        f"xwas/multivariate_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


def get_controls_tab_category_multivariate():
    categories = pd.Index(MAIN_CATEGORIES_TO_CATEGORIES["All"]).drop(MULTIVARIATE_CATEGORIES_TO_REMOVE)

    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_category_multivariate",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_category_multivariate", categories, "Select X subcategory: ", from_dict=False),
            get_item_radio_items("order_type_category_multivariate", ORDER_TYPES, "Order by:"),
            get_item_radio_items(
                "algorithm_category",
                {
                    "elastic_net": ALGORITHMS["elastic_net"],
                    "light_gbm": ALGORITHMS["light_gbm"],
                    "neural_network": ALGORITHMS["neural_network"],
                },
                "Select an Algorithm :",
            ),
            get_item_radio_items(
                "correlation_type_category_multivariate", CORRELATION_TYPES, "Select correlation type :"
            ),
        ]
    )


@APP.callback(
    [Output("category_category_multivariate", "options"), Output("category_category_multivariate", "value")],
    Input("main_category_category_multivariate", "value"),
)
def _change_category_category_multivariate(main_category):
    return (
        get_options_from_list(MAIN_CATEGORIES_TO_CATEGORIES[main_category]),
        MAIN_CATEGORIES_TO_CATEGORIES[main_category][0],
    )


@APP.callback(
    [
        Output("graph_category_multivariate", "figure"),
        Output("title_category_multivariate", "children"),
        Output("histogram_category_multivariate", "figure"),
    ],
    [
        Input("order_type_category_multivariate", "value"),
        Input("algorithm_category", "value"),
        Input("correlation_type_category_multivariate", "value"),
        Input("memory_category_multivariate", "data"),
        Input("memory_scores_category_multivariate", "data"),
    ],
)
def _fill_graph_tab_category_multivariate(order_by, algorithm, correlation_type, data_category, data_scores):
    correlations_raw = pd.DataFrame(data_category).set_index(
        ["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["algorithm", "correlation_type"]
    )
    correlations = correlations_raw[[(algorithm, correlation_type), (algorithm, "number_features")]]
    correlations.columns = ["correlation", "number_features"]
    correlations.reset_index(inplace=True)

    scores = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"])
    scores.drop(index=scores.index[~scores.index.isin(CUSTOM_DIMENSIONS)], inplace=True)
    scores.reset_index(["sub_subdimension", "algorithm"], drop=True, inplace=True)

    for number in [1, 2]:
        correlations.set_index([f"dimension_{number}", f"subdimension_{number}"], inplace=True)
        correlations[f"r2_{number}"] = scores["r2"]
        correlations[f"r2_std_{number}"] = scores["r2_std"]
        correlations.reset_index(inplace=True)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[DIMENSIONS_SUBDIMENSIONS_INDEXES, DIMENSIONS_SUBDIMENSIONS_INDEXES]
    np.fill_diagonal(table_correlations.values, np.nan)

    customdata_list = []
    for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", "number_features"]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            )
            .loc[DIMENSIONS_SUBDIMENSIONS_INDEXES, DIMENSIONS_SUBDIMENSIONS_INDEXES]
            .values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=DIMENSIONS_SUBDIMENSIONS_INDEXES, columns=DIMENSIONS_SUBDIMENSIONS_INDEXES)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R² from age prediction: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[2]:.3f} +- %{customdata[3]:.3f} <br>Number features: %{customdata[4]}<br><extra></extra>"

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
