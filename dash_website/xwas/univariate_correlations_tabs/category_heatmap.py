from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
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
    CUSTOM_ORDER,
    ORDER_DIMENSIONS,
)
from dash_website.xwas import SUBSET_METHODS


def get_category_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_category")),
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_category(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_category"),
                                    dcc.Graph(id="graph_category", config=DOWNLOAD_CONFIG),
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
                                    dcc.Graph(id="histogram_category", config=DOWNLOAD_CONFIG),
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
    Output("memory_category", "data"), [Input("main_category_category", "value"), Input("category_category", "value")]
)
def _modify_store_category(main_category, category):
    if category == "All":
        category = f"All_{main_category}"

    return load_feather(
        f"xwas/univariate_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


def get_controls_tab_category():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_category",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_category", ["All"], "Select X subcategory: ", from_dict=False),
            get_item_radio_items("order_type_category", ORDER_TYPES, "Order by:"),
            get_item_radio_items("subset_method_category", SUBSET_METHODS, "Select subset method :"),
            get_item_radio_items("correlation_type_category", CORRELATION_TYPES, "Select correlation type :"),
        ]
    )


@APP.callback(
    [Output("category_category", "options"), Output("category_category", "value")],
    Input("main_category_category", "value"),
)
def _change_category_category(main_category):
    return get_options(["All"] + MAIN_CATEGORIES_TO_CATEGORIES[main_category]), "All"


@APP.callback(
    [Output("graph_category", "figure"), Output("title_category", "children"), Output("histogram_category", "figure")],
    [
        Input("order_type_category", "value"),
        Input("subset_method_category", "value"),
        Input("correlation_type_category", "value"),
        Input("memory_category", "data"),
    ],
)
def _fill_graph_tab_category(order_by, subset_method, correlation_type, data_category):
    correlations_raw = pd.DataFrame(data_category).set_index(
        ["dimension_1", "subdimension_1", "r2_1", "r2_std_1", "dimension_2", "subdimension_2", "r2_2", "r2_std_2"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations = correlations_raw[[(subset_method, correlation_type), (subset_method, "number_variables")]]
    correlations.columns = ["correlation", "number_variables"]
    correlations.reset_index(inplace=True)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]
    np.fill_diagonal(table_correlations.values, np.nan)

    customdata_list = []
    for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", "number_variables"]:
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

    hovertemplate = "Correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R2: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R2: %{customdata[2]:.3f} +- %{customdata[3]:.3f} <br>Number variables: %{customdata[4]}<br><extra></extra>"

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
        width=1500,
        height=1500,
    )

    return (
        fig,
        f"Average correlation = {correlations['correlation'].mean().round(3)} +- {correlations['correlation'].std().round(3)}",
        histogram_correlation(table_correlations),
    )
