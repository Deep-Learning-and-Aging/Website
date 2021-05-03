from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items
from dash_website import CORRELATION_TYPES, MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS
from dash_website.xwas import SUBSET_METHODS
from dash_website.correlation_between import DATA_TYPES, AGGREGATE_TYPES, ORDER_TYPES


def get_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_heatmap")),
            html.H1("Correlation between accelerated aging dimensions"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_heatmap(),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_heatmap"),
                                    dcc.Graph(id="graph_heatmap"),
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
    Output("memory_heatmap", "data"), [Input("data_type_heatmap", "value"), Input("aggregate_type_heatmap", "value")]
)
def _modify_store_heatmap(data_type, aggregate_type):
    return load_feather(
        f"correlation_between_accelerated_aging_dimensions/{aggregate_type}_{data_type}.feather"
    ).to_dict()


def get_controls_tab_heatmap():
    return dbc.Card(
        [
            get_item_radio_items("data_type_heatmap", DATA_TYPES, "Select the data type: "),
            get_item_radio_items("aggregate_type_heatmap", AGGREGATE_TYPES, "Select aggregate type: ", from_dict=False),
            get_item_radio_items("order_type_heatmap", ORDER_TYPES, "Order by:"),
        ]
    )


@APP.callback(
    [Output("graph_heatmap", "figure"), Output("title_heatmap", "children")],
    [Input("order_type_heatmap", "value"), Input("memory_heatmap", "data")],
)
def _fill_graph_tab_category(order_by, data_heatmap):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations_raw = pd.DataFrame(data_heatmap).set_index(["dimension_1", "dimension_2"])
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
