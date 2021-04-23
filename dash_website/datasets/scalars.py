from re import S
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website.datasets import TREE_SCALARS, ETHNICITIES, SEX_VALUE


def get_layout():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_scalars")),
            html.H1("Datasets - Scalars"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dbc.Card(get_controls_scalars())), justify="center"),
            dbc.Row(dbc.Col(dbc.Card(get_subcontrols_scalars())), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_distribution_scalars"),
                        dcc.Graph(id="scalars_distribution_scalars"),
                    ]
                ),
                justify="center",
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_values_scalars"),
                        dcc.Graph(id="scalars_values_scalars"),
                    ]
                )
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_volcano_scalars"),
                        dcc.Graph(id="scalars_volcano_scalars"),
                    ]
                )
            ),
        ],
        fluid=True,
    )


@APP.callback(
    Output("memory_scalars", "data"),
    [
        Input("dimension_scalars", "value"),
        Input("subdimension_scalars", "value"),
        Input("sub_subdimension_scalars", "value"),
    ],
)
def _modify_store_scalars(dimension, subdimension, sub_subdimension):
    return load_feather(f"datasets/scalars/{dimension}_{subdimension}_{sub_subdimension}.feather").to_dict()


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


def get_subcontrols_scalars():
    return [
        get_drop_down(
            "feature_scalars",
            [""],
            "Select feature :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [Output("feature_scalars", "options"), Output("feature_scalars", "value")], Input("memory_scalars", "data")
)
def _change_feature(scalars_data):
    features = pd.DataFrame(scalars_data).columns.drop(["id", "sex", "chronological_age"] + ETHNICITIES)

    return get_options(features), features[0]


@APP.callback(
    [Output("scalars_distribution_scalars", "figure"), Output("title_distribution_scalars", "children")],
    [
        Input("feature_scalars", "value"),
        Input("memory_scalars", "data"),
    ],
)
def _change_figure(feature, data_scalars):
    import plotly.graph_objs as go

    scalars = pd.DataFrame(data_scalars).set_index(["sex", "id"])

    fig = go.Figure()

    fig.add_histogram(
        x=scalars.loc[SEX_VALUE["female"], feature], name="Females", histnorm="percent", marker=dict(color="pink")
    )

    fig.add_histogram(
        x=scalars.loc[SEX_VALUE["male"], feature], name="Males", histnorm="percent", marker=dict(color="blue")
    )

    fig.update_layout(
        width=2000, height=500, xaxis_title_text="Value", yaxis_title_text="Count", bargap=0.2, bargroupgap=0.1
    )

    return fig, feature