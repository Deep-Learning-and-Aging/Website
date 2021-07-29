import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import numpy as np
import pandas as pd

from dash_website.app import APP
from dash_website.utils.controls import (
    get_item_radio_items,
    get_drop_down,
    get_options_from_list,
)
from dash_website.utils.aws_loader import load_feather
from dash_website import (
    DOWNLOAD_CONFIG,
    MAIN_CATEGORIES_TO_CATEGORIES,
    RENAME_DIMENSIONS,
    GRAPH_SIZE,
    DIMENSIONS_SUBDIMENSIONS,
)
from dash_website.xwas.univariate_results_tabs import VOLCANO_TABLE_COLUMNS


def get_univariate_volcano():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_univariate_volcano")]),
            html.H1("Univariate associations - XWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab_univariate_volcano(), html.Br(), html.Br()], width={"size": 3}),
                    dbc.Col(
                        dcc.Loading(
                            [html.H2("Volcano plot"), dcc.Graph(id="graph_univariate_volcano", config=DOWNLOAD_CONFIG)]
                        ),
                        width={"size": 9},
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            [
                                dash_table.DataTable(
                                    id="table_univariate_volcano",
                                    columns=[{"id": key, "name": name} for key, name in VOLCANO_TABLE_COLUMNS.items()],
                                    style_cell={"textAlign": "left"},
                                    sort_action="custom",
                                    sort_mode="single",
                                )
                            ]
                        ),
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab_univariate_volcano():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_univariate_volcano",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_univariate_volcano", ["All"], "Select X subcategory: ", from_dict=False),
            get_drop_down(
                "dimension_univariate_volcano",
                DIMENSIONS_SUBDIMENSIONS,
                "Select an aging dimension: ",
            ),
        ]
    )


@APP.callback(
    [Output("category_univariate_volcano", "options"), Output("category_univariate_volcano", "value")],
    Input("main_category_univariate_volcano", "value"),
)
def _change_controls_category(main_category):
    if main_category == "All":
        list_categories = list(pd.Index(MAIN_CATEGORIES_TO_CATEGORIES[main_category]).drop(["Genetics", "Phenotypic"]))
    else:
        list_categories = MAIN_CATEGORIES_TO_CATEGORIES[main_category]
    return get_options_from_list(["All"] + list_categories), "All"


@APP.callback(Output("memory_univariate_volcano", "data"), Input("dimension_univariate_volcano", "value"))
def _modify_store_univariate_volcano(dimension):
    return load_feather(
        f"xwas/univariate_results/linear_correlations_{RENAME_DIMENSIONS.get(dimension, dimension)}.feather"
    ).to_dict()


@APP.callback(
    Output("graph_univariate_volcano", "figure"),
    [
        Input("main_category_univariate_volcano", "value"),
        Input("category_univariate_volcano", "value"),
        Input("memory_univariate_volcano", "data"),
    ],
)
def _fill_volcano_plot_univariate_volcano(main_category, category, dict_correlations):
    import plotly.express as px
    import plotly.graph_objects as go

    correlations = pd.DataFrame(dict_correlations).set_index(["category", "variable"])

    if category == "All":
        correlations_category = correlations.loc[
            correlations.index.get_level_values("category").isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])
        ]
    else:
        correlations_category = correlations.loc[correlations.index.get_level_values("category").isin([category])]

    correlations_category["neg_log_p_value"] = -np.log10(
        correlations_category["p_value"] + np.nextafter(np.float64(0), np.float64(1))
    )
    correlations_category["category"] = correlations_category.index.get_level_values("category")
    correlations_category["variable"] = correlations_category.index.get_level_values("variable")

    correlations_category["p_value"] = correlations_category["p_value"].apply(lambda x: "%.3e" % x)

    fig = px.scatter(
        correlations_category,
        x="correlation",
        y="neg_log_p_value",
        custom_data=["variable", "p_value", "sample_size"],
        color="category",
        labels={"correlation": "Partial Correlation", "neg_log_p_value": "-log(p-value)", "category": "Categories:"},
    )
    fig.update_traces(
        hovertemplate="<br>".join(
            [
                "Variable: %{customdata[0]}",
                "Partial Correlation: %{x:.3f}",
                "p-value: %{customdata[1]:.3E}",
                "Samples size: %{customdata[2]}",
            ]
        )
    )

    x_range_min = correlations_category["correlation"].min() - correlations_category["correlation"].std()
    x_range_max = correlations_category["correlation"].max() + correlations_category["correlation"].std()
    fig.add_trace(
        go.Scatter(
            x=[x_range_min, x_range_max],
            y=[-np.log10(0.05), -np.log10(0.05)],
            mode="lines",
            name="No Correction",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=[x_range_min, x_range_max],
            y=[-np.log10(0.05 / correlations_category.shape[0]), -np.log10(0.05 / correlations_category.shape[0])],
            mode="lines",
            name="With Bonferoni Correction",
        )
    )
    fig.update_layout(
        width=GRAPH_SIZE,
        height=1000,
        xaxis_range=[x_range_min, x_range_max],
        xaxis_title_font={"size": 25},
        yaxis_title_font={"size": 25},
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return fig


@APP.callback(
    Output("table_univariate_volcano", "data"),
    [
        Input("memory_univariate_volcano", "data"),
        Input("main_category_univariate_volcano", "value"),
        Input("category_univariate_volcano", "value"),
        Input("table_univariate_volcano", "sort_by"),
    ],
)
def _sort_table_univariate_volcano(dict_correlations, main_category, category, sort_by_col):
    correlations = pd.DataFrame(dict_correlations).set_index(["category", "variable"])

    if category == "All":
        correlations_category = correlations.loc[
            correlations.index.get_level_values("category").isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])
        ].copy()
    else:
        correlations_category = correlations.loc[correlations.index.get_level_values("category").isin([category])]

    correlations_category.reset_index(inplace=True)

    if sort_by_col is not None and len(sort_by_col) > 0:
        is_ascending = sort_by_col[0]["direction"] == "asc"
        correlations_category.sort_values(sort_by_col[0]["column_id"], ascending=is_ascending, inplace=True)
    else:
        correlations_category.sort_values("p_value", inplace=True)

    correlations_category["p_value"] = correlations_category["p_value"].apply(lambda x: "%.3e" % x)
    correlations_category[pd.Index(VOLCANO_TABLE_COLUMNS.keys()).drop("p_value")] = correlations_category[
        pd.Index(VOLCANO_TABLE_COLUMNS.keys()).drop("p_value")
    ].round(3)

    return correlations_category.to_dict("records")
