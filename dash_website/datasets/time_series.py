from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather, load_npy
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website.datasets import (
    TREE_TIME_SERIES,
    INFORMATION_TIME_SERIES,
    SEX_LEGEND,
    AGE_GROUP_LEGEND,
    SAMPLE_LEGEND,
    AGE_RANGES,
)


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_time_series", data=get_data())]),
            html.H1("Datasets - Time series"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dbc.Card(get_controls_time_series())), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(get_controls_side_time_series("left")), style={"width": 6}),
                    dbc.Col(dbc.Card(get_controls_side_time_series("right")), style={"width": 6}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            [
                                html.H3(id="title_left_time_series"),
                                dcc.Graph(id="time_series_left_time_series"),
                            ]
                        ),
                        style={"width": 6},
                    ),
                    dbc.Col(
                        dcc.Loading(
                            [
                                html.H3(id="title_right_time_series"),
                                dcc.Graph(id="time_series_right_time_series"),
                            ]
                        ),
                        style={"width": 6},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather("datasets/time_series/information.feather").to_dict()


def get_controls_time_series():
    first_dimension = list(TREE_TIME_SERIES.keys())[0]
    first_subdimension = list(TREE_TIME_SERIES[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_time_series", list(TREE_TIME_SERIES.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_time_series",
            list(TREE_TIME_SERIES[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_drop_down(
            "sub_subdimension_time_series",
            TREE_TIME_SERIES[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_time_series", "options"),
        Output("subdimension_time_series", "value"),
        Output("sub_subdimension_time_series", "options"),
        Output("sub_subdimension_time_series", "value"),
    ],
    [Input("dimension_time_series", "value"), Input("subdimension_time_series", "value")],
)
def _change_subdimensions(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_time_series":
        first_subdimension = list(TREE_TIME_SERIES[dimension].keys())[0]
        return (
            get_options(list(TREE_TIME_SERIES[dimension].keys())),
            list(TREE_TIME_SERIES[dimension].keys())[0],
            get_options(TREE_TIME_SERIES[dimension][first_subdimension]),
            TREE_TIME_SERIES[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_TIME_SERIES[dimension].keys())),
            subdimension,
            get_options(TREE_TIME_SERIES[dimension][subdimension]),
            TREE_TIME_SERIES[dimension][subdimension][0],
        )


def get_controls_side_time_series(side):
    first_dimension = list(TREE_TIME_SERIES.keys())[0]
    first_subdimension = list(TREE_TIME_SERIES[first_dimension].keys())[0]
    first_sub_subdimension = TREE_TIME_SERIES[first_dimension][first_subdimension][0]
    nb_channel = INFORMATION_TIME_SERIES[first_dimension][first_subdimension][first_sub_subdimension]["nb_channel"]

    return [
        get_item_radio_items(f"sex_{side}_time_series", SEX_LEGEND, "Select sex :"),
        get_item_radio_items(f"age_group_{side}_time_series", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down(f"sample_{side}_time_series", SAMPLE_LEGEND, "Select sample :"),
        get_drop_down(f"channel_{side}_time_series", range(nb_channel), "Select channel :", from_dict=False),
    ]


@APP.callback(
    [
        Output("channel_left_time_series", "options"),
        Output("channel_left_time_series", "value"),
        Output("channel_right_time_series", "options"),
        Output("channel_right_time_series", "value"),
    ],
    [
        Input("dimension_time_series", "value"),
        Input("subdimension_time_series", "value"),
        Input("sub_subdimension_time_series", "value"),
    ],
)
def _change_channel(dimension, subdimension, sub_subdimension):
    nb_channel = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["nb_channel"]

    return [get_options(range(nb_channel)), 0, get_options(range(nb_channel)), 0]


@APP.callback(
    [Output("time_series_left_time_series", "figure"), Output("title_left_time_series", "children")],
    [
        Input("dimension_time_series", "value"),
        Input("subdimension_time_series", "value"),
        Input("sub_subdimension_time_series", "value"),
        Input("sex_left_time_series", "value"),
        Input("age_group_left_time_series", "value"),
        Input("sample_left_time_series", "value"),
        Input("channel_left_time_series", "value"),
        Input("memory_time_series", "data"),
    ],
)
def _display_left_time_series(
    dimension, subdimension, sub_subdimension, sex, age_group, sample, channel, data_time_series
):
    return display_time_series(
        dimension, subdimension, sub_subdimension, sex, age_group, sample, channel, data_time_series
    )


@APP.callback(
    [Output("time_series_right_time_series", "figure"), Output("title_right_time_series", "children")],
    [
        Input("dimension_time_series", "value"),
        Input("subdimension_time_series", "value"),
        Input("sub_subdimension_time_series", "value"),
        Input("sex_right_time_series", "value"),
        Input("age_group_right_time_series", "value"),
        Input("sample_right_time_series", "value"),
        Input("channel_right_time_series", "value"),
        Input("memory_time_series", "data"),
    ],
)
def _display_right_time_series(
    dimension, subdimension, sub_subdimension, sex, age_group, sample, channel, data_time_series
):
    return display_time_series(
        dimension, subdimension, sub_subdimension, sex, age_group, sample, channel, data_time_series
    )


def display_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, channel, data_time_series):
    import plotly.graph_objs as go

    chronological_age = (
        pd.DataFrame(data_time_series)
        .set_index(["dimension", "subdimension", "sub_subdimension", "sex", "age_group", "aging_rate", "sample"])
        .loc[
            (dimension, subdimension, sub_subdimension, sex, age_group, "normal", int(sample)),
            ["chronological_age"],
        ]
        .tolist()
    )
    index_in_age_ranges = np.searchsorted(AGE_RANGES, chronological_age)

    title = f"The participant is between {AGE_RANGES[index_in_age_ranges - 1][0]} and {AGE_RANGES[index_in_age_ranges][0]} years old"

    path_to_time_series = (
        f"datasets/time_series/{dimension}/{subdimension}/{sub_subdimension}/{sex}/{age_group}/sample_{sample}.npy"
    )

    time_series = load_npy(path_to_time_series)

    if time_series.ndim > 1:
        channel_time_series = time_series[int(channel)]
    else:
        channel_time_series = time_series

    scatter = go.Scatter(y=channel_time_series, mode="markers", marker={"size": 5})

    fig = go.Figure(scatter)

    x_label = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["x_label"]
    y_label = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["y_label"]

    fig.update_layout(
        {
            "xaxis": {"title": x_label},
            "yaxis": {"title": y_label},
        }
    )

    return fig, title
