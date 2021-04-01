from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
)
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, DIMENSIONS


def get_category_heatmap():
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
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


def get_controls_tab():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_category", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_category"),
            get_subset_method_radio_items("subset_method_correlations"),
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
        Input("correlation_type_category", "value"),
        Input("memory_correlations", "data"),
    ],
)
def _fill_graph_tab_category(main_category, category, correlation_type, data):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations = pd.DataFrame(data).set_index(["dimension_1", "dimension_2", "category"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["subset_method", "observation"]
    )

    if category == "All":
        category = f"All_{main_category}"

    matrix_correlations_2d = correlations[correlation_type].swaplevel().swaplevel(i=0, j=1).loc[category, "mean"]
    matrix_correlations_2d.name = "correlation"
    matrix_correlations_2d_trim = matrix_correlations_2d.loc[DIMENSIONS]
    correlations_2d = pd.pivot_table(
        matrix_correlations_2d_trim.to_frame(),
        values="correlation",
        index="dimension_1",
        columns="dimension_2",
        dropna=False,
    ).fillna(0)
    correlations_2d[DIMENSIONS[0]] = 0  # add correlations of 0 since upper matrix

    correlations_values = correlations_2d.loc[DIMENSIONS, DIMENSIONS].values
    correlations_values[np.tril_indices(correlations_values.shape[0], -1)] = correlations_values.T[
        np.tril_indices(correlations_values.shape[0], -1)
    ]
    correlations_2d.loc[DIMENSIONS, DIMENSIONS] = correlations_values

    matrix_number_variables_2d = (
        correlations["number_variables"].swaplevel().swaplevel(i=0, j=1).loc[category, "number_variables"]
    )
    matrix_number_variables_2d.name = "number_variables"
    matrix_number_variables_2d_trim = matrix_number_variables_2d.loc[DIMENSIONS]
    number_variables_2d = pd.pivot_table(
        matrix_number_variables_2d_trim.to_frame(),
        values="number_variables",
        index="dimension_1",
        columns="dimension_2",
        dropna=False,
    ).fillna(0)
    number_variables_2d[DIMENSIONS[0]] = 0  # add correlations of 0 since upper matrix

    number_variables_values = number_variables_2d.loc[DIMENSIONS, DIMENSIONS].values
    number_variables_values[np.tril_indices(number_variables_values.shape[0], -1)] = number_variables_values.T[
        np.tril_indices(number_variables_values.shape[0], -1)
    ]
    number_variables_2d.loc[DIMENSIONS, DIMENSIONS] = number_variables_values.astype(int)

    fig = create_dendrogram_heatmap(
        correlations_2d.loc[DIMENSIONS, DIMENSIONS], number_variables_2d.loc[DIMENSIONS, DIMENSIONS]
    )

    fig.update_layout(
        {
            "xaxis": {"title": "Aging dimension", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "Aging dimension", "showgrid": False},
        }
    )

    return fig, "Average correlation = ??? ± ???"
