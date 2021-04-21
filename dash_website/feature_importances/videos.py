from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_options_from_dict, get_item_radio_items, get_drop_down
from dash_website.datasets import CHAMBERS_LEGEND, SEX_LEGEND, AGE_GROUP_LEGEND, SAMPLE_LEGEND, SEX_TO_PRONOUN


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_videos_features", data=get_data())]),
            html.H1("Feature importances - Videos"),
            html.Br(),
            html.Br(),
            dbc.Row(get_controls_videos(), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(get_controls_left_video()), style={"width": 6}),
                    dbc.Col(dbc.Card(get_controls_right_video()), style={"width": 6}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H3(id="title_left_video_features"), dcc.Loading(id="gif_display_left_video_features")],
                        style={"width": 6},
                    ),
                    dbc.Col(
                        [html.H3(id="title_right_video_features"), dcc.Loading(id="gif_display_right_video_features")],
                        style={"width": 6},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather("datasets/videos/information.feather").to_dict()


def get_controls_videos():
    return [
        dbc.Col(html.H4("Heart MRI with :"), width="auto"),
        dbc.Col(
            dcc.RadioItems(
                id="chamber_type_features",
                options=get_options_from_dict(CHAMBERS_LEGEND),
                value=list(CHAMBERS_LEGEND.keys())[0],
                labelStyle={"display": "inline-block", "margin": "5px"},
            )
        ),
    ]


def get_controls_left_video():
    return [
        get_item_radio_items("sex_left_video_features", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_left_video_features", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_left_video_features", SAMPLE_LEGEND, "Select sample :"),
    ]


def get_controls_right_video():
    return [
        get_item_radio_items("sex_right_video_features", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_right_video_features", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_right_video_features", SAMPLE_LEGEND, "Select sample :"),
    ]


@APP.callback(
    [Output("gif_display_left_video_features", "children"), Output("title_left_video_features", "children")],
    [
        Input("chamber_type_features", "value"),
        Input("sex_left_video_features", "value"),
        Input("age_left_video_features", "value"),
        Input("sample_left_video_features", "value"),
        Input("memory_videos_features", "data"),
    ],
)
def _display_left_gif_features(chamber_type, sex, age_group, sample, data_videos):
    return display_gif_features(chamber_type, sex, age_group, sample, data_videos)


@APP.callback(
    [Output("gif_display_right_video_features", "children"), Output("title_right_video_features", "children")],
    [
        Input("chamber_type_features", "value"),
        Input("sex_right_video_features", "value"),
        Input("age_right_video_features", "value"),
        Input("sample_right_video_features", "value"),
        Input("memory_videos_features", "data"),
    ],
)
def _display_right_gif_features(chamber_type, sex, age_group, sample, data_videos):
    return display_gif_features(chamber_type, sex, age_group, sample, data_videos)


def display_gif_features(chamber_type, sex, age_group, sample, data_videos):
    chronological_age, ethnicity = (
        pd.DataFrame(data_videos)
        .set_index(["chamber", "sex", "age_group", "sample"])
        .loc[(int(chamber_type), sex, age_group, int(sample)), ["chronological_age", "ethnicity"]]
        .tolist()
    )
    title = f"The participant is {chronological_age} years old, {SEX_TO_PRONOUN[sex]} ethnicity is {ethnicity}."

    gif_display = html.Div(
        gif.GifPlayer(
            gif=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.gif",
            still=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.png",
        ),
        style={"padding-left": 400},
    )
    return gif_display, title