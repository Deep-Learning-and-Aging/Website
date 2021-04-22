from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather, load_src_image, does_key_exists
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website.datasets import (
    TREE_TIME_SERIES,
    SIDES_DIMENSION,
    SIDES_SUBDIMENSION_EXCEPTION,
    SEX_LEGEND,
    AGE_GROUP_LEGEND,
    SAMPLE_LEGEND,
    SEX_TO_PRONOUN,
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
                    dbc.Col(dbc.Card(get_controls_left_time_series()), style={"width": 6}),
                    dbc.Col(dbc.Card(get_controls_right_time_series()), style={"width": 6}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H3(id="title_left_time_series"), dcc.Loading(id="time_series_left_time_series")],
                        style={"width": 6},
                    ),
                    dbc.Col(
                        [html.H3(id="title_right_time_series"), dcc.Loading(id="time_series_right_time_series")],
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


def get_controls_left_time_series():
    return [
        get_item_radio_items("sex_left_time_series", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_group_left_time_series", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_left_time_series", SAMPLE_LEGEND, "Select sample :"),
    ]


def get_controls_right_time_series():
    return [
        get_item_radio_items("sex_right_time_series", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_group_right_time_series", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_right_time_series", SAMPLE_LEGEND, "Select sample :"),
    ]


@APP.callback(
    [Output("time_series_left_time_series", "children"), Output("title_left_time_series", "children")],
    [
        Input("dimension_time_series", "value"),
        Input("subdimension_time_series", "value"),
        Input("sub_subdimension_time_seriesmages", "value"),
        Input("sex_left_time_series", "value"),
        Input("age_group_left_time_series", "value"),
        Input("sample_left_time_series", "value"),
        Input("memory_time_series", "data"),
    ],
)
def _display_left_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, data_time_series):
    return display_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, data_time_series)


@APP.callback(
    [Output("time_series_right_time_series", "children"), Output("title_right_time_series", "children")],
    [
        Input("dimension_time_series", "value"),
        Input("subdimension_time_series", "value"),
        Input("sub_subdimension_time_series", "value"),
        Input("sex_right_time_series", "value"),
        Input("age_group_right_time_series", "value"),
        Input("sample_right_time_series", "value"),
        Input("memory_time_series", "data"),
    ],
)
def _display_right_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, data_time_series):
    return display_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, data_time_series)


def display_time_series(dimension, subdimension, sub_subdimension, sex, age_group, sample, data_time_series):
    chronological_age, ethnicity = (
        pd.DataFrame(data_time_series)
        .set_index(["dimension", "subdimension", "sub_subdimension", "sex", "age_group", "aging_rate", "sample"])
        .loc[
            (dimension, subdimension, sub_subdimension, sex, age_group, "normal", int(sample)),
            ["chronological_age", "ethnicity"],
        ]
        .tolist()
    )
    title = f"The participant is {chronological_age} years old, {SEX_TO_PRONOUN[sex]} ethnicity is {ethnicity}."

    path_to_time_series = (
        f"datasets/time_series/{dimension}/{subdimension}/{sub_subdimension}/{sex}/{age_group}/sample_{sample}.npy"
    )

    if does_key_exists(path_to_time_series):
        time_series = html.Img(
            src=load_src_image(path_to_time_series),
            style={"height": 800, "margin": "15px", "padding-left": 100},
        )
    else:
        time_series = html.Div()
        title = "The time_series was not provided by the UK Biobank dataset, please choose another sample."

    return time_series, title
