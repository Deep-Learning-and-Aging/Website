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
    TREE_DIMENSIONS,
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
                        [html.H3(id="title_left_image"), dcc.Loading(id="image_left_image")],
                        style={"width": 6},
                    ),
                    dbc.Col(
                        [html.H3(id="title_right_image"), dcc.Loading(id="image_right_image")],
                        style={"width": 6},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather("datasets/images/information.feather").to_dict()


def get_controls_images():
    first_dimension = list(TREE_DIMENSIONS.keys())[0]
    first_subdimension = list(TREE_DIMENSIONS[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_images", list(TREE_DIMENSIONS.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_images",
            list(TREE_DIMENSIONS[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_drop_down(
            "sub_subdimension_images",
            TREE_DIMENSIONS[first_dimension][first_subdimension],
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
        first_subdimension = list(TREE_DIMENSIONS[dimension].keys())[0]
        return (
            get_options(list(TREE_DIMENSIONS[dimension].keys())),
            list(TREE_DIMENSIONS[dimension].keys())[0],
            get_options(TREE_DIMENSIONS[dimension][first_subdimension]),
            TREE_DIMENSIONS[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_DIMENSIONS[dimension].keys())),
            subdimension,
            get_options(TREE_DIMENSIONS[dimension][subdimension]),
            TREE_DIMENSIONS[dimension][subdimension][0],
        )


def get_controls_left_image():
    return [
        get_item_radio_items("sex_left_image", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_range_left_image", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_left_image", SAMPLE_LEGEND, "Select sample :"),
    ]


def get_controls_right_image():
    return [
        get_item_radio_items("sex_right_image", SEX_LEGEND, "Select sex :"),
        get_item_radio_items("age_range_right_image", AGE_GROUP_LEGEND, "Select age group :"),
        get_drop_down("sample_right_image", SAMPLE_LEGEND, "Select sample :"),
    ]


@APP.callback(
    [Output("image_left_image", "children"), Output("title_left_image", "children")],
    [
        Input("dimension_images", "value"),
        Input("subdimension_images", "value"),
        Input("sub_subdimension_images", "value"),
        Input("sex_left_image", "value"),
        Input("age_range_left_image", "value"),
        Input("sample_left_image", "value"),
        Input("memory_images", "data"),
    ],
)
def _display_left_image(dimension, subdimension, sub_subdimension, sex, age_range, sample, data_images):
    return display_image(dimension, subdimension, sub_subdimension, sex, age_range, sample, data_images)


@APP.callback(
    [Output("image_right_image", "children"), Output("title_right_image", "children")],
    [
        Input("dimension_images", "value"),
        Input("subdimension_images", "value"),
        Input("sub_subdimension_images", "value"),
        Input("sex_right_image", "value"),
        Input("age_range_right_image", "value"),
        Input("sample_right_image", "value"),
        Input("memory_images", "data"),
    ],
)
def _display_right_image(dimension, subdimension, sub_subdimension, sex, age_range, sample, data_images):
    return display_image(dimension, subdimension, sub_subdimension, sex, age_range, sample, data_images)


def display_image(dimension, subdimension, sub_subdimension, sex, age_range, sample, data_images):
    chronological_age, ethnicity = (
        pd.DataFrame(data_images)
        .set_index(["dimension", "subdimension", "sub_subdimension", "sex", "age_group", "aging_rate", "sample"])
        .loc[
            (dimension, subdimension, sub_subdimension, sex, age_range, "normal", int(sample)),
            ["chronological_age", "ethnicity"],
        ]
        .tolist()
    )
    title = f"The participant is {chronological_age} years old, {SEX_TO_PRONOUN[sex]} ethnicity is {ethnicity}."

    if dimension in SIDES_DIMENSION and sub_subdimension not in SIDES_SUBDIMENSION_EXCEPTION:
        left_path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_range}/normal/left_sample_{sample}.jpg"
        right_path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_range}/normal/right_sample_{sample}.jpg"

        missing_left = False
        missing_right = False
        if does_key_exists(left_path_to_image):
            left_image = html.Img(
                src=load_src_image(left_path_to_image),
                style={"height": 600, "margin": "2px"},
            )
        else:
            left_image = html.Div()
            missing_left = True

        if does_key_exists(right_path_to_image):
            right_image = html.Img(
                src=load_src_image(right_path_to_image),
                style={"height": 600, "margin": "2px", "-webkit-transform": "scaleX(-1)", "transform": "scaleX(-1)"},
            )
        else:
            right_image = html.Div()
            missing_right = True

        if missing_left and missing_right:
            image = html.Div()
            title = "The image was not provided by the UK Biobank dataset, please choose another sample."
        else:
            image = html.Div([left_image, right_image], style={"margin": "15px", "padding-left": 100})

    else:
        path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_range}/normal/sample_{sample}.jpg"

        if does_key_exists(path_to_image):
            image = html.Img(
                src=load_src_image(path_to_image),
                style={"height": 800, "margin": "15px", "padding-left": 100},
            )
        else:
            image = html.Div()
            title = "The image was not provided by the UK Biobank dataset, please choose another sample."

    return image, title
