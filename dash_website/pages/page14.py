import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import (
    get_dataset_options,
    ETHNICITY_COLS,
    get_colorscale,
    dict_dataset_images_to_organ_and_view,
    empty_graph,
    read_img,
    load_csv,
)
import pandas as pd
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
import plotly.express as px
from dash_website.app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64
from io import BytesIO
from dash.exceptions import PreventUpdate

aging_rate = "Normal"
path_attention_maps = "page9_AttentionMaps/Images"
path_attention_maps_metadata = "page9_AttentionMaps/Attention_maps_infos/"
if MODE != "All":
    organ_select = dbc.FormGroup(
        [
            html.P("Select Organ : "),
            dcc.Dropdown(
                id="select_organ_image", options=get_dataset_options([MODE]), placeholder="Select an organ", value=MODE
            ),
            html.Br(),
        ],
        style={"display": "None"},
    )
else:
    organ_select = dbc.FormGroup(
        [
            html.P("Select Organ : "),
            dcc.Dropdown(
                id="select_organ_image",
                options=get_dataset_options(dict_dataset_images_to_organ_and_view.keys()),
                placeholder="Select an organ",
            ),
            html.Br(),
        ]
    )

controls = dbc.Card(
    [
        organ_select,
        dbc.FormGroup(
            [
                html.P("Select View : "),
                dcc.Dropdown(id="select_view_image", options=get_dataset_options([]), placeholder="Select a view"),
                html.Br(),
            ]
        ),
        dbc.FormGroup(
            [
                html.P("Select Transformation : "),
                dcc.Dropdown(
                    id="select_transformation_image",
                    options=get_dataset_options([]),
                    placeholder="Select a transformation",
                ),
                html.Br(),
            ]
        ),
        dbc.Button("Reset", id="reset_page14", className="mr-2", color="primary"),
    ]
)


@app.callback(
    [
        Output("select_organ_image", "value"),
        Output("select_view_image", "value"),
        Output("select_transformation_image", "value"),
    ],
    [Input("reset_page14", "n_clicks")],
)
def reset(n):
    if n:
        if n > 0:
            return [None, None, None]
    else:
        raise PreventUpdate()


controls_1 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select Sex : "),
                                dcc.Dropdown(
                                    id="select_sex_image_1",
                                    options=get_dataset_options(["Male", "Female"]),
                                    placeholder="Select a sex",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select an age group : "),
                                dcc.Dropdown(
                                    id="select_age_group_image_1",
                                    options=get_dataset_options(["Young", "Middle", "Old"]),
                                    placeholder="Select an age group",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select a sample : "),
                                dcc.Dropdown(
                                    id="select_sample_image_1",
                                    options=get_dataset_options([i for i in range(10)]),
                                    placeholder="Select a sample",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)
controls_2 = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select Sex : "),
                                dcc.Dropdown(
                                    id="select_sex_image_2",
                                    options=get_dataset_options(["Male", "Female"]),
                                    placeholder="Select a sex",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select an age group : "),
                                dcc.Dropdown(
                                    id="select_age_group_image_2",
                                    options=get_dataset_options(["Young", "Middle", "Old"]),
                                    placeholder="Select an age group",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                dbc.Col(
                    [
                        dbc.FormGroup(
                            [
                                html.P("Select a sample : "),
                                dcc.Dropdown(
                                    id="select_sample_image_2",
                                    options=get_dataset_options([i for i in range(10)]),
                                    placeholder="Select a sample",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
            ]
        )
    ]
)


@app.callback(
    Output("select_transformation_image", "options"),
    [Input("select_organ_image", "value"), Input("select_view_image", "value")],
)
def generate_list_view_list(value_organ, value_view):
    if value_view is None:
        return [{"value": "", "label": ""}]
    else:
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value_organ][value_view])


@app.callback(Output("select_view_image", "options"), [Input("select_organ_image", "value")])
def generate_list_view_list(value):
    if value is None:
        return [{"value": "", "label": ""}]
    else:
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value])


layout = html.Div(
    [
        html.H1("Datasets - Images"),
        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col([controls], md=3),
                        dbc.Col(
                            [
                                controls_1,
                                dcc.Loading(html.Div(id="row_image_1")),
                                controls_2,
                                dcc.Loading(html.Div(id="row_image_2")),
                            ],
                            md=9,
                        ),
                    ]
                )
            ],
            # style={"height": "100vh"},
            fluid=True,
        ),
    ]
)


@app.callback(
    Output("row_image_1", "children"),
    [
        Input("select_organ_image", "value"),
        Input("select_view_image", "value"),
        Input("select_transformation_image", "value"),
        Input("select_sex_image_1", "value"),
        Input("select_age_group_image_1", "value"),
        Input("select_sample_image_1", "value"),
    ],
)
def _plot_images_1(organ, view, transformation, sex, age_group, sample):  # , aging_rate):
    if None not in [organ, view, transformation, sex, age_group, aging_rate, sample]:
        path_metadata = path_attention_maps_metadata + "AttentionMaps-samples_Age_%s_%s_%s.csv" % (
            organ,
            view,
            transformation,
        )
        df_metadata = load_csv(path_metadata)
        df_metadata = df_metadata[
            (df_metadata.sex == sex)
            & (df_metadata.age_category == age_group.lower())
            & (df_metadata.aging_rate == aging_rate.lower())
            & (df_metadata["sample"] == sample)
        ]
        title = "Chronological Age = %.2f" % (df_metadata["Age"].iloc[0])
        if (organ, view) in [
            ("Eyes", "Fundus"),
            ("Eyes", "OCT"),
            ("Arterial", "Carotids"),
            ("Musculoskeletal", "Knees"),
            ("Musculoskeletal", "Hips"),
        ]:

            path_image_left = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "left/RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s_left.jpg" % sample
            )
            path_image_right = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "right/RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s_right.jpg" % sample
            )

            count = [True, True]
            try:
                raw_left = read_img(path_image_left)
            except FileNotFoundError:
                count[0] = False
            try:
                raw_right = read_img(path_image_right)
            except FileNotFoundError:
                count[1] = False

            if count[0]:
                final_left = Image.fromarray((raw_left).astype(np.uint8)).convert("RGB")
                buffered_left = BytesIO()
                final_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode("ascii")
                src_left = "data:image/png;base64,{}".format(img_base64_left)
            if count[1]:
                final_right = Image.fromarray((raw_right).astype(np.uint8)).convert("RGB")
                final_right = final_right.transpose(Image.FLIP_LEFT_RIGHT)
                buffered_right = BytesIO()
                final_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode("ascii")
                src_right = "data:image/png;base64,{}".format(img_base64_right)

            if count[0] and not count[1]:
                final_right = Image.new("RGBA", (raw_left.shape[1], raw_left.shape[0]))
                buffered_right = BytesIO()
                final_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode("ascii")
                src_right = "data:image/png;base64,{}".format(img_base64_right)
            elif not count[0] and count[1]:
                final_left = Image.new("RGBA", (raw_right.shape[1], raw_right.shape[0]))
                buffered_left = BytesIO()
                final_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode("ascii")
                src_left = "data:image/png;base64,{}".format(img_base64_left)

            col = [
                dbc.Row([html.H3(title), html.Br()]),
                dbc.Row(
                    [
                        dbc.Col(
                            [html.Img(id="attentionmap_left", style={"height": "100%", "width": "100%"}, src=src_left)]
                        ),
                        dbc.Col(
                            [
                                html.Img(
                                    id="attentionmap_right", style={"height": "100%", "width": "100%"}, src=src_right
                                )
                            ]
                        ),
                    ]
                ),
            ]
            return col

        else:
            path_image = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s.jpg" % sample
            )
            raw = read_img(path_image)
            raw = Image.fromarray((raw).astype(np.uint8)).convert("RGB")
            buffered = BytesIO()
            raw.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")
            src = "data:image/png;base64,{}".format(img_base64)
            col = [
                html.H3(title),
                html.Br(),
                html.Img(id="attentionmap", style={"height": "50%", "width": "50%"}, src=src),
            ]
            return col
    else:
        return [dcc.Graph(figure=Figure(empty_graph))]


@app.callback(
    Output("row_image_2", "children"),
    [
        Input("select_organ_image", "value"),
        Input("select_view_image", "value"),
        Input("select_transformation_image", "value"),
        Input("select_sex_image_2", "value"),
        Input("select_age_group_image_2", "value"),
        Input("select_sample_image_2", "value"),
    ],
)
def _plot_images_2(organ, view, transformation, sex, age_group, sample):  # , aging_rate):
    if None not in [organ, view, transformation, sex, age_group, aging_rate, sample]:
        path_metadata = path_attention_maps_metadata + "AttentionMaps-samples_Age_%s_%s_%s.csv" % (
            organ,
            view,
            transformation,
        )
        df_metadata = load_csv(path_metadata)
        df_metadata = df_metadata[
            (df_metadata.sex == sex)
            & (df_metadata.age_category == age_group.lower())
            & (df_metadata.aging_rate == aging_rate.lower())
            & (df_metadata["sample"] == sample)
        ]
        title = "Chronological Age = %.2f" % (df_metadata["Age"].iloc[0])
        if (organ, view) in [
            ("Eyes", "Fundus"),
            ("Eyes", "OCT"),
            ("Arterial", "Carotids"),
            ("Musculoskeletal", "Knees"),
            ("Musculoskeletal", "Hips"),
        ]:
            path_image_left = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "left/RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s_left.jpg" % sample
            )
            path_image_right = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "right/RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s_right.jpg" % sample
            )

            count = [True, True]
            try:
                raw_left = read_img(path_image_left)
            except FileNotFoundError:
                count[0] = False
            try:
                raw_right = read_img(path_image_right)
            except FileNotFoundError:
                count[1] = False

            if count[0]:
                final_left = Image.fromarray((raw_left).astype(np.uint8)).convert("RGB")
                buffered_left = BytesIO()
                final_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode("ascii")
                src_left = "data:image/png;base64,{}".format(img_base64_left)
            if count[1]:
                final_right = Image.fromarray((raw_right).astype(np.uint8)).convert("RGB")
                final_right = final_right.transpose(Image.FLIP_LEFT_RIGHT)
                buffered_right = BytesIO()
                final_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode("ascii")
                src_right = "data:image/png;base64,{}".format(img_base64_right)

            if count[0] and not count[1]:
                final_right = Image.new("RGBA", (raw_left.shape[1], raw_left.shape[0]))
                buffered_right = BytesIO()
                final_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode("ascii")
                src_right = "data:image/png;base64,{}".format(img_base64_right)
            elif not count[0] and count[1]:
                final_left = Image.new("RGBA", (raw_right.shape[1], raw_right.shape[0]))
                buffered_left = BytesIO()
                final_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode("ascii")
                src_left = "data:image/png;base64,{}".format(img_base64_left)

            col = [
                dbc.Row([html.H3(title), html.Br()]),
                dbc.Row(
                    [
                        dbc.Col(
                            [html.Img(id="attentionmap_left", style={"height": "100%", "width": "100%"}, src=src_left)]
                        ),
                        dbc.Col(
                            [
                                html.Img(
                                    id="attentionmap_right", style={"height": "100%", "width": "100%"}, src=src_right
                                )
                            ]
                        ),
                    ]
                ),
            ]
            return col

        else:
            path_image = (
                path_attention_maps
                + "/%s/%s/%s/%s/%s/%s/" % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
                + "RawImage_Age_"
                + organ
                + "_"
                + view
                + "_"
                + transformation
                + "_"
                + sex
                + "_"
                + age_group.lower()
                + "_"
                + aging_rate.lower()
                + "_%s.jpg" % sample
            )
            raw = read_img(path_image)
            raw = Image.fromarray((raw).astype(np.uint8)).convert("RGB")
            buffered = BytesIO()
            raw.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode("ascii")
            src = "data:image/png;base64,{}".format(img_base64)
            col = [
                html.H3(title),
                html.Br(),
                html.Img(id="attentionmap", style={"height": "50%", "width": "50%"}, src=src),
            ]
            return col
    else:
        return [dcc.Graph(figure=Figure(empty_graph))]
