from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website import DOWNLOAD_CONFIG, CORRELATION_TYPES, MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS
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
                        md=3,
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
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
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
    [Output("graph_category", "figure"), Output("title_category", "children")],
    [
        Input("subset_method_category", "value"),
        Input("correlation_type_category", "value"),
        Input("memory_category", "data"),
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
