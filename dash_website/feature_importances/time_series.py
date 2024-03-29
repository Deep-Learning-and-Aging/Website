from datetime import time
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather, load_npy
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options_from_list
from dash_website import DOWNLOAD_CONFIG, ALGORITHMS
from dash_website.datasets import (
    TREE_TIME_SERIES,
    INFORMATION_TIME_SERIES,
    SEX_LEGEND,
    AGE_GROUP_LEGEND,
    SAMPLE_LEGEND,
)
from dash_website.feature_importances import AGING_RATE_LEGEND


def get_controls_time_series_features():
    first_dimension = list(TREE_TIME_SERIES.keys())[0]
    first_subdimension = list(TREE_TIME_SERIES[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_time_series_features",
            list(TREE_TIME_SERIES.keys()),
            "Select main aging dimesion :",
            from_dict=False,
        ),
        get_item_radio_items(
            "subdimension_time_series_features",
            list(TREE_TIME_SERIES[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_drop_down(
            "sub_subdimension_time_series_features",
            TREE_TIME_SERIES[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_time_series_features", "options"),
        Output("subdimension_time_series_features", "value"),
        Output("sub_subdimension_time_series_features", "options"),
        Output("sub_subdimension_time_series_features", "value"),
        Output("title_time_series_features", "children"),
    ],
    [
        Input("dimension_time_series_features", "value"),
        Input("subdimension_time_series_features", "value"),
        Input("memory_scores_features", "data"),
    ],
)
def _change_subdimensions_time_series_features(dimension, subdimension, data_scores):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_time_series_features":
        first_subdimension = list(TREE_TIME_SERIES[dimension].keys())[0]

        option_subdimension = get_options_from_list(list(TREE_TIME_SERIES[dimension].keys()))
        value_subdimension = list(TREE_TIME_SERIES[dimension].keys())[0]
        option_sub_subdimension = get_options_from_list(TREE_TIME_SERIES[dimension][first_subdimension])
        value_sub_subdimension = TREE_TIME_SERIES[dimension][first_subdimension][0]
    else:
        option_subdimension = get_options_from_list(list(TREE_TIME_SERIES[dimension].keys()))
        value_subdimension = subdimension
        option_sub_subdimension = get_options_from_list(TREE_TIME_SERIES[dimension][subdimension])
        value_sub_subdimension = TREE_TIME_SERIES[dimension][subdimension][0]

    scores_raw = (
        pd.DataFrame(data_scores)
        .set_index(["dimension", "subdimension", "sub_subdimension"])
        .loc[(dimension, value_subdimension, value_sub_subdimension)]
        .set_index("algorithm")
    )
    scores = (
        scores_raw.drop(index=scores_raw.index[scores_raw.index == "*"]).sort_values("r2", ascending=False).round(3)
    )

    title = ""
    for algorithm in scores.index:
        title += f"The {ALGORITHMS[algorithm]} has a R² of {scores.loc[algorithm, 'r2']} +- {scores.loc[algorithm, 'r2_std']}. "

    return option_subdimension, value_subdimension, option_sub_subdimension, value_sub_subdimension, title


def get_controls_side_time_series_features(side):
    first_dimension = list(TREE_TIME_SERIES.keys())[0]
    first_subdimension = list(TREE_TIME_SERIES[first_dimension].keys())[0]
    first_sub_subdimension = TREE_TIME_SERIES[first_dimension][first_subdimension][0]
    nb_channel = INFORMATION_TIME_SERIES[first_dimension][first_subdimension][first_sub_subdimension]["nb_channel"]

    if side == "left":
        value_idx = 0
    else:  # side == "right":
        value_idx = 1
    return [
        get_item_radio_items(f"sex_{side}_time_series_features", SEX_LEGEND, "Select sex :", value_idx=value_idx),
        get_item_radio_items(
            f"age_group_{side}_time_series_features", AGE_GROUP_LEGEND, "Select age group :", value_idx=1
        ),
        get_item_radio_items(
            f"aging_rate_{side}_time_series_features", AGING_RATE_LEGEND, "Select aging rate :", value_idx=1
        ),
        get_drop_down(f"sample_{side}_time_series_features", SAMPLE_LEGEND, "Select sample :"),
        get_drop_down(f"channel_{side}_time_series_features", range(nb_channel), "Select channel :", from_dict=False),
    ]


@APP.callback(
    [
        Output("channel_left_time_series_features", "options"),
        Output("channel_left_time_series_features", "value"),
        Output("channel_right_time_series_features", "options"),
        Output("channel_right_time_series_features", "value"),
    ],
    [
        Input("dimension_time_series_features", "value"),
        Input("subdimension_time_series_features", "value"),
        Input("sub_subdimension_time_series_features", "value"),
    ],
)
def _change_channel_time_series_features(dimension, subdimension, sub_subdimension):
    nb_channel = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["nb_channel"]

    return [get_options_from_list(range(nb_channel)), 0, get_options_from_list(range(nb_channel)), 0]


@APP.callback(
    [Output("time_series_left_time_series_features", "figure"), Output("title_left_time_series_features", "children")],
    [
        Input("dimension_time_series_features", "value"),
        Input("subdimension_time_series_features", "value"),
        Input("sub_subdimension_time_series_features", "value"),
        Input("sex_left_time_series_features", "value"),
        Input("age_group_left_time_series_features", "value"),
        Input("aging_rate_left_time_series_features", "value"),
        Input("sample_left_time_series_features", "value"),
        Input("channel_left_time_series_features", "value"),
        Input("memory_time_series_features", "data"),
    ],
)
def _display_left_time_series_features(
    dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample, channel, data_time_series
):
    return display_time_series_features(
        dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample, channel, data_time_series
    )


@APP.callback(
    [
        Output("time_series_right_time_series_features", "figure"),
        Output("title_right_time_series_features", "children"),
    ],
    [
        Input("dimension_time_series_features", "value"),
        Input("subdimension_time_series_features", "value"),
        Input("sub_subdimension_time_series_features", "value"),
        Input("sex_right_time_series_features", "value"),
        Input("age_group_right_time_series_features", "value"),
        Input("aging_rate_right_time_series_features", "value"),
        Input("sample_right_time_series_features", "value"),
        Input("channel_right_time_series_features", "value"),
        Input("memory_time_series_features", "data"),
    ],
)
def _display_right_time_series_features(
    dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample, channel, data_time_series
):
    return display_time_series_features(
        dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample, channel, data_time_series
    )


def display_time_series_features(
    dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, sample, channel, data_time_series
):
    import plotly.graph_objs as go

    chronological_age, biological_age = (
        pd.DataFrame(data_time_series)
        .set_index(["dimension", "subdimension", "sub_subdimension", "sex", "age_group", "aging_rate", "sample"])
        .loc[
            (dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, int(sample)),
            ["chronological_age", "biological_age"],
        ]
        .tolist()
    )

    title = f"The participant is an {aging_rate} ager: {np.round_(biological_age - chronological_age, 1)} years"

    path_to_time_series = f"datasets/time_series/{dimension}/{subdimension}/{sub_subdimension}/{sex}/{age_group}/{aging_rate}/sample_{sample}.npy"

    time_series = load_npy(path_to_time_series)[int(channel)]

    scatter = go.Scatter(
        y=time_series[0],
        mode="markers",
        marker={
            "size": 5,
            "color": time_series[1],
            "showscale": True,
        },
    )
    fig = go.Figure(scatter)

    x_label = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["x_label"]
    y_label = INFORMATION_TIME_SERIES[dimension][subdimension][sub_subdimension]["y_label"]

    fig.update_layout(
        {
            "xaxis": {"title": x_label},
            "xaxis_title_font": {"size": 25},
            "yaxis": {"title": y_label},
            "yaxis_title_font": {"size": 25},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    return fig, title


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(
                    id="memory_time_series_features",
                    data=load_feather("datasets/time_series/information.feather").to_dict(),
                ),
                dcc.Store(
                    id="memory_scores_features",
                    data=load_feather(
                        "age_prediction_performances/scores_all_samples_per_participant.feather"
                    ).to_dict(),
                ),
            ]
        ),
        html.H1("Model interpretability - Time series"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_time_series_features())), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(html.H3(id="title_time_series_features"), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_side_time_series_features("left")), width={"size": 6}),
                dbc.Col(dbc.Card(get_controls_side_time_series_features("right")), width={"size": 6}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        [
                            html.H3(id="title_left_time_series_features"),
                            dcc.Graph(id="time_series_left_time_series_features", config=DOWNLOAD_CONFIG),
                        ]
                    ),
                    width={"size": 6},
                ),
                dbc.Col(
                    dcc.Loading(
                        [
                            html.H3(id="title_right_time_series_features"),
                            dcc.Graph(id="time_series_right_time_series_features", config=DOWNLOAD_CONFIG),
                        ]
                    ),
                    width={"size": 6},
                ),
            ]
        ),
    ],
    fluid=True,
)
