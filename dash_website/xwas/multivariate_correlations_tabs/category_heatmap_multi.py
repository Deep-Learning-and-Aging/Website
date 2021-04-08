from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
)
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS


def get_category_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_category_multi")),
            html.H1("Multivariate XWAS - Correlations between accelerated aging"),
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
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_category_multi"),
                                    dcc.Graph(id="graph_category_multi"),
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


@APP.callback(
    Output("memory_category_multi", "data"),
    [Input("main_category_category_multi", "value"), Input("category_category_multi", "value")],
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
            get_main_category_radio_items("main_category_category_multi", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_category_multi"),
            get_subset_method_radio_items("subset_method_category_multi"),
            get_correlation_type_radio_items("correlation_type_category_multi"),
        ]
    )


@APP.callback(
    [Output("category_category_multi", "options"), Output("category_category_multi", "value")],
    Input("main_category_category_multi", "value"),
)
def _change_category_category(main_category):
    return get_options(["All"] + MAIN_CATEGORIES_TO_CATEGORIES[main_category]), "All"


@APP.callback(
    [Output("graph_category_multi", "figure"), Output("title_category_multi", "children")],
    [
        Input("subset_method_category_multi", "value"),
        Input("correlation_type_category_multi", "value"),
        Input("memory_category_multi", "data"),
    ],
)
def _fill_graph_tab_category(subset_method, correlation_type, data_category):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations_raw = pd.DataFrame(data_category).set_index(["dimension_1", "dimension_2"])
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations = correlations_raw[[(subset_method, correlation_type)]]
    correlations.columns = ["correlation"]
    numbers_variables = correlations_raw[[(subset_method, "number_variables")]]
    numbers_variables.columns = ["number_variables"]

    correlations_2d = pd.pivot_table(
        correlations, values="correlation", index="dimension_1", columns="dimension_2", dropna=False
    ).fillna(0)
    correlations_2d.rename(index=RENAME_DIMENSIONS, columns=RENAME_DIMENSIONS, inplace=True)
    numbers_variables_2d = pd.pivot_table(
        numbers_variables, values="number_variables", index="dimension_1", columns="dimension_2", dropna=False
    ).fillna(0)
    numbers_variables_2d.rename(index=RENAME_DIMENSIONS, columns=RENAME_DIMENSIONS, inplace=True)

    fig = create_dendrogram_heatmap(correlations_2d, numbers_variables_2d)

    fig.update_layout(
        {
            "xaxis": {"title": "Aging dimension", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "Aging dimension", "showgrid": False},
        }
    )

    title_mean = correlations_2d.values[np.triu_indices(correlations_2d.shape[0], 1)].mean().round(3)
    title_std = correlations_2d.values[np.triu_indices(correlations_2d.shape[0], 1)].std().round(3)

    return fig, f"Average correlation = {title_mean} ± {title_std}"
