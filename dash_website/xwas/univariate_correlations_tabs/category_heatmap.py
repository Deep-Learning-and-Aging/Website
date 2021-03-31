from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
)
from dash_website.utils.aws_loader import load_feather
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES


def get_category_heatmap():
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dcc.Store(id="memory_category", data=get_data()),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [
                            html.H2(id="title_category"),
                            dcc.Graph(id="graph_category"),
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather(f"xwas/univariate_correlations/correlations.feather").to_dict()


def get_controls_tab():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_category", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_category"),
            get_subset_method_radio_items("subset_method_category"),
            get_correlation_type_radio_items("correlation_type_category"),
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
        Input("main_category_category", "value"),
        Input("category_category", "value"),
        Input("subset_method_category", "value"),
        Input("correlation_type_category", "value"),
        Input("memory_category", "data"),
    ],
)
def _fill_graph_tab_x(main_category, category, subset_method, correlation_type, data):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations = pd.DataFrame(data).set_index(["dimension_1", "dimension_2", "category"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["category", "variable"]
    )

    if category == "All":
        category = f"All_{main_category}"

    matrix_correlations_2d = (
        correlations[(subset_method, correlation_type)].swaplevel().swaplevel(i=0, j=1).loc[category]
    )
    matrix_correlations_2d.name = "correlation"
    correlations_2d = pd.pivot_table(
        matrix_correlations_2d.to_frame(), values="correlation", index="dimension_1", columns="dimension_2"
    ).fillna(0)

    matrix_number_variables_2d = (
        correlations[(subset_method, "number_variables")].swaplevel().swaplevel(i=0, j=1).loc[category]
    )
    matrix_number_variables_2d.name = "number_variables"
    number_variables_2d = pd.pivot_table(
        matrix_number_variables_2d.to_frame(), values="number_variables", index="dimension_1", columns="dimension_2"
    ).fillna(0)

    return create_dendrogram_heatmap(correlations_2d, number_variables_2d), "Average correlation = ??? ± ???"
