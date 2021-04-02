from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.controls import get_main_category_radio_items, get_category_drop_down, get_options
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS


def get_category_heatmap(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_category(subset_method_radio_items, correlation_type_radio_items),
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
                                    dcc.Graph(id="graph_category"),
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


def get_controls_tab_category(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_category", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_category"),
            subset_method_radio_items,
            correlation_type_radio_items,
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
        Input("memory_correlations", "data"),
        Input("memory_number_variables", "data"),
    ],
)
def _fill_graph_tab_category(main_category, category, data_correlations, data_number_variables):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations = pd.DataFrame(data_correlations).set_index(["dimension_1", "dimension_2", "category"])
    number_variables = pd.DataFrame(data_number_variables).set_index(["dimension_1", "dimension_2", "category"])

    if category == "All":
        category = f"All_{main_category}"

    correlations_category = correlations.swaplevel().swaplevel(i=0, j=1).loc[category]
    number_variables_category = number_variables.swaplevel().swaplevel(i=0, j=1).loc[category]

    correlations_2d = (
        pd.pivot_table(
            correlations_category, values="correlation", index="dimension_1", columns="dimension_2", dropna=False
        )
        .fillna(0)
        .rename(index=RENAME_DIMENSIONS, columns=RENAME_DIMENSIONS)
    )
    number_variables_2d = (
        pd.pivot_table(
            number_variables_category,
            values="number_variables",
            index="dimension_1",
            columns="dimension_2",
            dropna=False,
        )
        .fillna(0)
        .rename(index=RENAME_DIMENSIONS, columns=RENAME_DIMENSIONS)
    )

    fig = create_dendrogram_heatmap(correlations_2d, number_variables_2d)

    fig.update_layout(
        {
            "xaxis": {"title": "Aging dimension", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "Aging dimension", "showgrid": False},
        }
    )

    title_mean = correlations_2d.values[np.triu_indices(correlations_2d.shape[0], 1)].mean().round(3)
    title_std = correlations_2d.values[np.triu_indices(correlations_2d.shape[0], 1)].std().round(3)

    return fig, f"Average correlation = {title_mean} ± {title_std}"
