from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_options_from_dict, get_item_radio_items, get_drop_down, get_options
from dash_website.datasets import CHAMBERS_LEGEND, SEX_LEGEND, AGE_GROUP_LEGEND, SAMPLE_LEGEND, SEX_TO_PRONOUN
from dash_website.datasets import TREE_CHOICES


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_images", data=get_data())]),
            html.H1("Datasets - Images"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dbc.Card(get_controls_images())), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                [
                    dbc.Col(dbc.Card(get_controls_left_image()), style={"width": 6}),
                    dbc.Col(dbc.Card(get_controls_right_image()), style={"width": 6}),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [html.H3(id="title_left_image"), dcc.Loading(id="gif_display_left_image")],
                        style={"width": 6},
                    ),
                    dbc.Col(
                        [html.H3(id="title_right_image"), dcc.Loading(id="gif_display_right_image")],
                        style={"width": 6},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather("datasets/videos/information.feather").to_dict()


def get_controls_images():
    first_dimension = list(TREE_CHOICES.keys())[0]
    first_subdimension = list(TREE_CHOICES[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_images", list(TREE_CHOICES.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_images", list(TREE_CHOICES[first_dimension].keys()), "Select subdimension :", from_dict=False
        ),
        get_drop_down(
            "sub_subdimension_images",
            TREE_CHOICES[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_images", "options"),
        Output("subdimension_images", "value"),
        Output("sub_subdimension_images", "options"),
        Output("sub_subdimension_images", "value"),
    ],
    [Input("dimension_images", "value"), Input("subdimension_images", "value")],
)
def _change_subdimensions(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_images":
        first_subdimension = list(TREE_CHOICES[dimension].keys())[0]
        return (
            get_options(list(TREE_CHOICES[dimension].keys())),
            list(TREE_CHOICES[dimension].keys())[0],
            get_options(TREE_CHOICES[dimension][first_subdimension]),
            TREE_CHOICES[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_CHOICES[dimension].keys())),
            subdimension,
            get_options(TREE_CHOICES[dimension][subdimension]),
            TREE_CHOICES[dimension][subdimension][0],
        )


def get_controls_left_image():
    return [
        get_item_radio_items("sex_left_image", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_left_image", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_left_image", SAMPLE_LEGEND, "Select sample :"),
    ]


def get_controls_right_image():
    return [
        get_item_radio_items("sex_right_image", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_right_image", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_right_image", SAMPLE_LEGEND, "Select sample :"),
    ]


"""@APP.callback(
    [Output("gif_display_left_image", "children"), Output("title_left_image", "children")],
    [
        Input("chamber_type", "value"),
        Input("sex_left_image", "value"),
        Input("age_left_image", "value"),
        Input("sample_left_image", "value"),
        Input("memory_images", "data"),
    ],
)
def _display_left_image(chamber_type, sex, age_group, sample, data_video):
    chronological_age, ethnicity = (
        pd.DataFrame(data_video)
        .set_index(["chamber", "sex", "age_group", "sample"])
        .loc[(int(chamber_type), sex, age_group, int(sample)), ["chronological_age", "ethnicity"]]
        .tolist()
    )
    title = f"Participants of {chronological_age} years old, {SEX_TO_PRONOUN[sex]} ethnicity is {ethnicity}."

    gif_display = html.Div(
        gif.GifPlayer(
            gif=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.gif",
            still=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.png",
        ),
        style={"padding-left": 400},
    )
    return gif_display, title


@APP.callback(
    [Output("gif_display_right_image", "children"), Output("title_right_image", "children")],
    [
        Input("chamber_type", "value"),
        Input("sex_right_image", "value"),
        Input("age_right_image", "value"),
        Input("sample_right_image", "value"),
        Input("memory_images", "data"),
    ],
)
def _display_right_image(chamber_type, sex, age_group, sample, data_video):
    chronological_age, ethnicity = (
        pd.DataFrame(data_video)
        .set_index(["chamber", "sex", "age_group", "sample"])
        .loc[(int(chamber_type), sex, age_group, int(sample)), ["chronological_age", "ethnicity"]]
        .tolist()
    )
    title = f"Participants of {chronological_age} years old, {SEX_TO_PRONOUN[sex]} ethnicity is {ethnicity}."

    gif_display = html.Div(
        gif.GifPlayer(
            gif=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.gif",
            still=f"../data/datasets/videos/{chamber_type}_chambers/{sex}/{age_group}/sample_{sample}.png",
        ),
        style={"padding-left": 400},
    )

    return gif_display, title"""