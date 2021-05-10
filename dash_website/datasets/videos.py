from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_options_from_dict, get_item_radio_items, get_drop_down
from dash_website.datasets import CHAMBERS_LEGEND, SEX_LEGEND, AGE_GROUP_LEGEND, SAMPLE_LEGEND, AGE_RANGES


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_videos", data=get_data())]),
            html.H1("Datasets - Videos"),
            html.Br(),
            html.Br(),
            dbc.Row(get_controls_videos(), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(get_controls_side_video("left")), width={"size": 6}),
                    dbc.Col(dbc.Card(get_controls_side_video("right")), width={"size": 6}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H3(id="title_left_video"), dcc.Loading(id="gif_display_left_video")],
                        width={"size": 6},
                    ),
                    dbc.Col(
                        [html.H3(id="title_right_video"), dcc.Loading(id="gif_display_right_video")],
                        width={"size": 6},
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
                id="chamber_type",
                options=get_options_from_dict(CHAMBERS_LEGEND),
                value=list(CHAMBERS_LEGEND.keys())[0],
                labelStyle={"display": "inline-block", "margin": "5px"},
            )
        ),
    ]


def get_controls_side_video(side):
    if side == "left":
        value_idx = 0
    else:  # side == "right":
        value_idx = 1

    return [
        get_item_radio_items(f"sex_{side}_video", SEX_LEGEND, "Select sex :", value_idx=value_idx),
        get_item_radio_items(f"age_{side}_video", AGE_GROUP_LEGEND, "Select age group :", value_idx=1),
        get_drop_down(f"sample_{side}_video", SAMPLE_LEGEND, "Select sample :"),
    ]


@APP.callback(
    [Output("gif_display_left_video", "children"), Output("title_left_video", "children")],
    [
        Input("chamber_type", "value"),
        Input("sex_left_video", "value"),
        Input("age_left_video", "value"),
        Input("sample_left_video", "value"),
        Input("memory_videos", "data"),
    ],
)
def _display_left_gif(chamber_type, sex, age_group, sample, data_videos):
    return display_gif(chamber_type, sex, age_group, sample, data_videos)


@APP.callback(
    [Output("gif_display_right_video", "children"), Output("title_right_video", "children")],
    [
        Input("chamber_type", "value"),
        Input("sex_right_video", "value"),
        Input("age_right_video", "value"),
        Input("sample_right_video", "value"),
        Input("memory_videos", "data"),
    ],
)
def _display_right_gif(chamber_type, sex, age_group, sample, data_videos):
    return display_gif(chamber_type, sex, age_group, sample, data_videos)


def display_gif(chamber_type, sex, age_group, sample, data_videos):
    chronological_age = (
        pd.DataFrame(data_videos)
        .set_index(["chamber", "sex", "age_group", "sample"])
        .loc[(int(chamber_type), sex, age_group, int(sample)), ["chronological_age"]]
        .tolist()
    )
    index_in_age_ranges = np.searchsorted(AGE_RANGES, chronological_age)

    title = f"The participant is between {AGE_RANGES[index_in_age_ranges - 1][0]} and {AGE_RANGES[index_in_age_ranges][0]} years old"

    gif_display = html.Div(
        gif.GifPlayer(
            gif=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.gif",
            still=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.png",
        ),
        style={"padding-left": 400},
    )
    return gif_display, title
