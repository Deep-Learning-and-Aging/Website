import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import numpy as np
import pandas as pd

from dash_website.app import APP
from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_dimension_drop_down,
    get_options,
)
from dash_website.utils.aws_loader import list_dir, load_feather
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES
from dash_website.xwas.univariate_results_tabs import VOLCANO_TABLE_COLUMNS


def get_volcano():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_volcano")]),
            html.H1("Univariate XWAS - Results"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col(dcc.Loading([dcc.Graph(id="graph_volcano")]), md=9),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id="table_volcano",
                                columns=[{"name": i, "id": i} for i in list(VOLCANO_TABLE_COLUMNS.values())],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ],
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_volcano", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_volcano"),
            get_dimension_drop_down("dimension_volcano", DIMENSIONS),
        ]
    )


@APP.callback(
    [Output("category_volcano", "options"), Output("category_volcano", "value")],
    Input("main_category_volcano", "value"),
)
def _change_controls_category(main_category):
    if main_category == "All":
        list_categories = list(pd.Index(MAIN_CATEGORIES_TO_CATEGORIES[main_category]).drop(["Genetics", "Phenotypic"]))
    else:
        list_categories = MAIN_CATEGORIES_TO_CATEGORIES[main_category]
    return get_options(["All"] + list_categories), "All"


@APP.callback(Output("memory_volcano", "data"), Input("dimension_volcano", "value"))
def _modify_store_volcano(dimension):
    correlations = load_feather(f"xwas/univariate_results/linear_correlations_{dimension}.feather")

    return correlations.drop(index=correlations.index[correlations["sample_size"] < 10]).to_dict()


@APP.callback(
    Output("graph_volcano", "figure"),
    [Input("main_category_volcano", "value"), Input("category_volcano", "value"), Input("memory_volcano", "data")],
)
def _fill_volcano_plot(main_category, category, dict_correlations):
    import plotly.express as px
    import plotly.graph_objects as go

    correlations = pd.DataFrame(dict_correlations).set_index(["category", "variable"])

    if category == "All":
        correlations_category = correlations.loc[
            correlations.index.get_level_values("category").isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])
        ]
    else:
        correlations_category = correlations.loc[correlations.index.get_level_values("category").isin([category])]

    correlations_category["neg_log_p_value"] = -np.log10(correlations_category["p_value"])
    correlations_category["category"] = correlations_category.index.get_level_values("category")
    correlations_category["variable"] = correlations_category.index.get_level_values("variable")

    fig = px.scatter(
        correlations_category,
        x="correlation",
        y="neg_log_p_value",
        custom_data=["variable", "p_value", "sample_size"],
        color="category",
        labels={"correlation": "Partial Correlation", "neg_log_p_value": "-log(p-value)", "category": "Categories:"},
        title="Volcano plot",
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
    fig.update_layout(xaxis_range=[x_range_min, x_range_max])

    return fig


@APP.callback(
    Output("table_volcano", "data"),
    [
        Input("memory_volcano", "data"),
        Input("main_category_volcano", "value"),
        Input("category_volcano", "value"),
        Input("table_volcano", "sort_by"),
    ],
)
def _sort_table(dict_correlations, main_category, category, sort_by_col):
    correlations = pd.DataFrame(dict_correlations).set_index(["category", "variable"])

    if category == "All":
        correlations_category = correlations.loc[
            correlations.index.get_level_values("category").isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])
        ].copy()
    else:
        correlations_category = correlations.loc[correlations.index.get_level_values("category").isin([category])]

    correlations_category.reset_index(inplace=True)

    correlations_category.rename(
        columns=VOLCANO_TABLE_COLUMNS,
        inplace=True,
    )

    if sort_by_col is not None and len(sort_by_col) > 0:
        is_ascending = sort_by_col[0]["direction"] == "asc"
        correlations_category.sort_values(sort_by_col[0]["column_id"], ascending=is_ascending, inplace=True)
    else:
        correlations_category.sort_values(VOLCANO_TABLE_COLUMNS["p_value"], inplace=True)

    return correlations_category.round(5).to_dict("records")