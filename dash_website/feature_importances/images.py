from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np
from PIL import Image
from io import BytesIO
import base64

from dash_website.utils.aws_loader import load_feather, load_npy, load_jpg, does_key_exists
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_check_list, get_options
from dash_website.datasets import (
    TREE_IMAGES,
    SIDES_DIMENSION,
    SIDES_SUBDIMENSION_EXCEPTION,
    SEX_LEGEND,
    AGE_GROUP_LEGEND,
    SAMPLE_LEGEND,
)
from dash_website.feature_importances import AGING_RATE_LEGEND, DISPLAY_MODE


def get_data_scores():
    return load_feather("feature_importances/scores_all_samples_per_participant.feather").to_dict()


def get_data_features():
    return load_feather("datasets/images/information.feather").to_dict()


def get_controls_images_features():
    first_dimension = list(TREE_IMAGES.keys())[0]
    first_subdimension = list(TREE_IMAGES[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_images_features", list(TREE_IMAGES.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_images_features",
            list(TREE_IMAGES[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_drop_down(
            "sub_subdimension_images_features",
            TREE_IMAGES[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
        get_check_list("display_mode_images_features", DISPLAY_MODE, "Select a display mode"),
    ]


@APP.callback(
    [
        Output("subdimension_images_features", "options"),
        Output("subdimension_images_features", "value"),
        Output("sub_subdimension_images_features", "options"),
        Output("sub_subdimension_images_features", "value"),
        Output("title_images_features", "children"),
    ],
    [
        Input("dimension_images_features", "value"),
        Input("subdimension_images_features", "value"),
        Input("memory_scores_features", "data"),
    ],
)
def _change_subdimensions_features(dimension, subdimension, data_scores):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_images_features":
        first_subdimension = list(TREE_IMAGES[dimension].keys())[0]

        option_subdimension = get_options(list(TREE_IMAGES[dimension].keys()))
        value_subdimension = list(TREE_IMAGES[dimension].keys())[0]
        option_sub_subdimension = get_options(TREE_IMAGES[dimension][first_subdimension])
        value_sub_subdimension = TREE_IMAGES[dimension][first_subdimension][0]
    else:
        option_subdimension = get_options(list(TREE_IMAGES[dimension].keys()))
        value_subdimension = subdimension
        option_sub_subdimension = get_options(TREE_IMAGES[dimension][subdimension])
        value_sub_subdimension = TREE_IMAGES[dimension][subdimension][0]

    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension"]).round(3)
    scores = (
        scores_raw.loc[(dimension, value_subdimension, value_sub_subdimension)]
        .set_index("algorithm")
        .sort_values("r2", ascending=False)
    )

    title = ""
    for algorithm in scores.index:
        title += f"The {algorithm} has a R2 of {scores.loc[algorithm, 'r2']} +- {scores.loc[algorithm, 'r2_std']}. "

    return option_subdimension, value_subdimension, option_sub_subdimension, value_sub_subdimension, title


def get_controls_side_image_features(side):
    if side == "left":
        value_idx = 0
    else:  # side == "right":
        value_idx = 1

    return [
        get_item_radio_items(f"sex_{side}_image_features", SEX_LEGEND, "Select sex :", value_idx=value_idx),
        get_item_radio_items(f"age_group_{side}_image_features", AGE_GROUP_LEGEND, "Select age group :", value_idx=1),
        get_item_radio_items(
            f"aging_rate_{side}_image_features", AGING_RATE_LEGEND, "Select aging rate :", value_idx=1
        ),
        get_drop_down(f"sample_{side}_image_features", SAMPLE_LEGEND, "Select sample :"),
    ]


@APP.callback(
    [Output("image_left_image_features", "children"), Output("title_left_image_features", "children")],
    [
        Input("dimension_images_features", "value"),
        Input("subdimension_images_features", "value"),
        Input("sub_subdimension_images_features", "value"),
        Input("display_mode_images_features", "value"),
        Input("sex_left_image_features", "value"),
        Input("age_group_left_image_features", "value"),
        Input("aging_rate_left_image_features", "value"),
        Input("sample_left_image_features", "value"),
        Input("memory_images_features", "data"),
    ],
)
def _display_left_image_features(
    dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rate, sample, data_images
):
    return display_image_features(
        dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rate, sample, data_images
    )


@APP.callback(
    [Output("image_right_image_features", "children"), Output("title_right_image_features", "children")],
    [
        Input("dimension_images_features", "value"),
        Input("subdimension_images_features", "value"),
        Input("sub_subdimension_images_features", "value"),
        Input("display_mode_images_features", "value"),
        Input("sex_right_image_features", "value"),
        Input("age_group_right_image_features", "value"),
        Input("aging_rate_right_image_features", "value"),
        Input("sample_right_image_features", "value"),
        Input("memory_images_features", "data"),
    ],
)
def _display_right_image_features(
    dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rage, sample, data_images
):
    return display_image_features(
        dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rage, sample, data_images
    )


def display_image_features(
    dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rate, sample, data_images
):
    chronological_age, biological_age = (
        pd.DataFrame(data_images)
        .set_index(["dimension", "subdimension", "sub_subdimension", "sex", "age_group", "aging_rate", "sample"])
        .loc[
            (dimension, subdimension, sub_subdimension, sex, age_group, aging_rate, int(sample)),
            ["chronological_age", "biological_age"],
        ]
        .tolist()
    )

    title = f"The participant is an {aging_rate} ager: {np.round_(biological_age - chronological_age, 1)} years"

    if dimension in SIDES_DIMENSION and subdimension not in SIDES_SUBDIMENSION_EXCEPTION:
        left_path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_group}/{aging_rate}/left_sample_{sample}.jpg"
        right_path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_group}/{aging_rate}/right_sample_{sample}.jpg"

        missing_left = False
        missing_right = False

        if len(display_mode) == 0:
            image = html.Div()
            title = "Please select a mode to display."
        else:
            if does_key_exists(left_path_to_image):
                left_source_image = get_image(
                    dimension,
                    subdimension,
                    sub_subdimension,
                    display_mode,
                    sex,
                    age_group,
                    aging_rate,
                    sample,
                    side="left_",
                )

                left_image = html.Img(
                    src=left_source_image,
                    style={"height": 400, "margin": "2px"},
                )
            else:
                left_image = html.Div()
                missing_left = True

            if does_key_exists(right_path_to_image):
                right_source_image = get_image(
                    dimension,
                    subdimension,
                    sub_subdimension,
                    display_mode,
                    sex,
                    age_group,
                    aging_rate,
                    sample,
                    side="right_",
                )

                right_image = html.Img(
                    src=right_source_image,
                    style={
                        "height": 400,
                        "margin": "2px",
                        "-webkit-transform": "scaleX(-1)",
                        "transform": "scaleX(-1)",
                    },
                )
            else:
                right_image = html.Div()
                missing_right = True

            if missing_left and missing_right:
                image = html.Div()
                title = "The image was not provided by the UK Biobank dataset, please choose another sample."
            else:
                image = html.Div([left_image, right_image], style={"margin": "15px", "padding-left": 50})

    else:
        path_to_image = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_group}/{aging_rate}/sample_{sample}.jpg"

        if len(display_mode) == 0:
            image = html.Div()
            title = "Please select a mode to display."
        elif does_key_exists(path_to_image):
            right_source_image = get_image(
                dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rate, sample
            )

            image = html.Img(
                src=right_source_image,
                style={"height": 800, "margin": "15px", "padding-left": 100},
            )
        else:
            image = html.Div()
            title = "The image was not provided by the UK Biobank dataset, please choose another sample."

    return image, title


def get_image(dimension, subdimension, sub_subdimension, display_mode, sex, age_group, aging_rate, sample, side=""):
    images = {}
    display_mode.sort()  # To put Saliency at the end and Gradcam in front of Raw

    if "Raw" in display_mode:
        path_to_raw = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Raw/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.jpg"
        images["Raw"] = load_jpg(path_to_raw)
    if "Gradcam" in display_mode:
        path_to_grad_cam = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Gradcam/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.npy"
        images["Gradcam"] = load_npy(path_to_grad_cam).astype(np.uint8)
    if "Saliency" in display_mode:
        path_to_saliency = f"datasets/images/{dimension}/{subdimension}/{sub_subdimension}/Saliency/{sex}/{age_group}/{aging_rate}/{side}sample_{sample}.npy"
        images["Saliency"] = load_npy(path_to_saliency).astype(np.uint8)

    if len(display_mode) == 1:
        image_to_display = Image.fromarray(images[display_mode[0]]).convert("RGBA")
    elif len(display_mode) == 2:
        if "Saliency" in display_mode:  # [0] = ? and [1] = Saliency since display mode is sorted
            image_to_display = Image.alpha_composite(
                Image.fromarray(images[display_mode[0]]).convert("RGBA"),
                Image.fromarray(images[display_mode[1]]),
            )
        else:  # [0] = "Gradcam" and [1] = "Raw" since display mode is sorted
            image_to_display = Image.fromarray(
                (0.3 * images[display_mode[0]] + 0.7 * images[display_mode[1]]).astype(np.uint8)
            ).convert("RGBA")
    else:  # if len(display_mode) == 3: # [0] = "Gradcam", [1] = "Raw", [2] = "Saliency" since display mode is sorted
        composite_image = Image.fromarray(
            (0.3 * images[display_mode[0]] + 0.7 * images[display_mode[1]]).astype(np.uint8)
        ).convert("RGBA")

        image_to_display = Image.alpha_composite(composite_image, Image.fromarray(images[display_mode[2]]))

    buffer = BytesIO()
    image_to_display.save(buffer, format="png")

    encoded_image = base64.b64encode(buffer.getvalue())

    return f"data:image/png;base64,{encoded_image.decode()}"


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_scores_features", data=get_data_scores()),
                dcc.Store(id="memory_images_features", data=get_data_features()),
            ]
        ),
        html.H1("Feature importances - Images"),
        html.Br(),
        html.Br(),
        dbc.Row(dbc.Col(dbc.Card(get_controls_images_features())), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(html.H2(id="title_images_features"), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_side_image_features("left")), width={"size": 6}),
                dbc.Col(dbc.Card(get_controls_side_image_features("right")), width={"size": 6}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.H3(id="title_left_image_features"), dcc.Loading(id="image_left_image_features")],
                    width={"size": 6},
                ),
                dbc.Col(
                    [html.H3(id="title_right_image_features"), dcc.Loading(id="image_right_image_features")],
                    width={"size": 6},
                ),
            ]
        ),
    ],
    fluid=True,
)
