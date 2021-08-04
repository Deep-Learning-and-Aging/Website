from re import sub
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options_from_list
from dash_website.utils.graphs import (
    heatmap_by_clustering,
    heatmap_by_sorted_dimensions,
    add_custom_legend_axis,
    histogram_correlation,
)
from dash_website import (
    DOWNLOAD_CONFIG,
    CORRELATION_TYPES,
    MAIN_CATEGORIES_TO_CATEGORIES,
    ORDER_TYPES,
    CUSTOM_DIMENSIONS,
    DIMENSIONS_SUBDIMENSIONS_INDEXES,
    GRAPH_SIZE,
)
from dash_website.xwas import SUBSET_METHODS


def get_heatmap_univariate_category():
    return dbc.Container(
        [
            dcc.Loading(
                [
                    dcc.Store(
                        id="memory_univariate_category",
                    ),
                    dcc.Store(
                        id="memory_scores_univariate_category",
                        data=load_feather(
                            "age_prediction_performances/scores_all_samples_per_participant.feather"
                        ).to_dict(),
                    ),
                ]
            ),
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_univariate_category(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_univariate_category"),
                                    dcc.Graph(id="graph_univariate_category", config=DOWNLOAD_CONFIG),
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
                                    dcc.Graph(id="histogram_univariate_category", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 9, "offset": 3},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


@APP.callback(
    Output("memory_univariate_category", "data"),
    [Input("main_category_univariate_category", "value"), Input("category_univariate_category", "value")],
)
def _modify_store_univariate_category(main_category, category):
    if category == "All":
        category = f"All_{main_category}"

    return load_feather(
        f"xwas/univariate_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


def get_controls_tab_univariate_category():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_univariate_category",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_univariate_category", ["All"], "Select X subcategory: ", from_dict=False),
            get_item_radio_items("order_type_univariate_category", ORDER_TYPES, "Order by:"),
            get_item_radio_items("subset_method_univariate_category", SUBSET_METHODS, "Select subset method :"),
            get_item_radio_items(
                "correlation_type_univariate_category", CORRELATION_TYPES, "Select correlation type :"
            ),
        ]
    )


@APP.callback(
    [Output("category_univariate_category", "options"), Output("category_univariate_category", "value")],
    Input("main_category_univariate_category", "value"),
)
def _change_category_category(main_category):
    return get_options_from_list(["All"] + MAIN_CATEGORIES_TO_CATEGORIES[main_category]), "All"


@APP.callback(
    [
        Output("graph_univariate_category", "figure"),
        Output("title_univariate_category", "children"),
        Output("histogram_univariate_category", "figure"),
    ],
    [
        Input("order_type_univariate_category", "value"),
        Input("subset_method_univariate_category", "value"),
        Input("correlation_type_univariate_category", "value"),
        Input("memory_univariate_category", "data"),
        Input("memory_scores_univariate_category", "data"),
    ],
)
def _fill_graph_tab_univariate_category(order_by, subset_method, correlation_type, data_category, data_scores):
    correlations_raw = pd.DataFrame(data_category).set_index(
        ["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations = correlations_raw[[(subset_method, correlation_type), (subset_method, "number_variables")]]
    correlations.columns = ["correlation", "number_variables"]
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
    for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", "number_variables"]:
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

    hovertemplate = "Correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[2]:.3f} +- %{customdata[3]:.3f} <br>Number variables: %{customdata[4]}<br><extra></extra>"

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
