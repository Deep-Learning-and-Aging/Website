from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website.datasets import TREE_SCALARS


def get_layout():
    return dbc.Container(
        [
            # dcc.Loading([dcc.Store(id="memory_scalars", data=get_data())]),
            html.H1("Datasets - Scalars"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dbc.Card(get_controls_scalars())), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H3(id="title_distribution_scalars"),
                        dcc.Graph(id="scalars_distribution_scalars"),
                    ]
                )
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H3(id="title_values_scalars"),
                        dcc.Graph(id="scalars_values_scalars"),
                    ]
                )
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H3(id="title_volcano_scalars"),
                        dcc.Graph(id="scalars_volcano_scalars"),
                    ]
                )
            ),
        ],
        fluid=True,
    )


# def get_data():
#     return load_feather("datasets/scalars/information.feather").to_dict()


def get_controls_scalars():
    first_dimension = list(TREE_SCALARS.keys())[0]
    first_subdimension = list(TREE_SCALARS[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_scalars", list(TREE_SCALARS.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_scalars",
            list(TREE_SCALARS[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_item_radio_items(
            "sub_subdimension_scalars",
            TREE_SCALARS[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_scalars", "options"),
        Output("subdimension_scalars", "value"),
        Output("sub_subdimension_scalars", "options"),
        Output("sub_subdimension_scalars", "value"),
    ],
    [Input("dimension_scalars", "value"), Input("subdimension_scalars", "value")],
)
def _change_subdimensions(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_scalars":
        first_subdimension = list(TREE_SCALARS[dimension].keys())[0]
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            list(TREE_SCALARS[dimension].keys())[0],
            get_options(TREE_SCALARS[dimension][first_subdimension]),
            TREE_SCALARS[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            subdimension,
            get_options(TREE_SCALARS[dimension][subdimension]),
            TREE_SCALARS[dimension][subdimension][0],
        )