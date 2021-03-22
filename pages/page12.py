import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output
from .tools import get_dataset_options, empty_graph, load_csv
import pandas as pd
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
import plotly.express as px
from dash.exceptions import PreventUpdate
from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64
from io import BytesIO

sample = 0
path_img = "page12_AttentionMapsVideos/img/"
path_gif = "page12_AttentionMapsVideos/gif/"
path_attention_maps_videos = "page12_AttentionMapsVideos/AttentionMapsVideos/"


path_score_scalar = "page2_predictions/Performances/PERFORMANCES_tuned_alphabetical_eids_Age_test.csv"
score = load_csv(path_score_scalar)

controls = dbc.Card(
    [
        dbc.FormGroup(
            [
                html.P("Select Organ : "),
                dcc.Dropdown(
                    id="select_organ_attention_video",
                    options=get_dataset_options(["Heart"]),
                    placeholder="Select an organ",
                    value="Heart",
                ),
                html.Br(),
            ]
        ),
        dbc.FormGroup(
            [
                html.P("Select View : "),
                dcc.Dropdown(
                    id="select_view_attention_video",
                    options=get_dataset_options(["MRI"]),
                    placeholder="Select a view",
                    value="MRI",
                ),
                html.Br(),
            ]
        ),
        dbc.FormGroup(
            [
                html.P("Select Transformation : "),
                dcc.Dropdown(
                    id="select_transformation_attention_video",
                    options=get_dataset_options(["3chambersRaw", "4chambersRaw"]),
                    placeholder="Select a transformation",
                ),
                html.Br(),
            ]
        ),
        dbc.Button("Reset", id="reset_page12", className="mr-2", color="primary"),
    ]
)


@app.callback(
    [
        Output("select_organ_attention_video", "value"),
        Output("select_view_attention_video", "value"),
        Output("select_transformation_attention_video", "value"),
    ],
    [Input("reset_page12", "n_clicks")],
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
                                html.P("Select sex : "),
                                dcc.Dropdown(
                                    id="select_sex_attention_video_1",
                                    options=[{"value": 0, "label": "Female"}, {"value": 1, "label": "Male"}],
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
                                    id="select_age_group_attention_video_1",
                                    options=get_dataset_options(["Young", "Middle", "Old"]),
                                    placeholder="Select an age group : ",
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
                                html.P("Select an aging rate : "),
                                dcc.Dropdown(
                                    id="select_aging_rate_attention_video_1",
                                    options=get_dataset_options(["Decelerated", "Normal", "Accelerated"]),
                                    placeholder="Select an aging rate",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                # dbc.Col([
                #     dbc.FormGroup([
                #         html.P("Select sample : "),
                #         dcc.Dropdown(
                #             id = 'select_sample_attention_video_1',
                #             options = get_dataset_options(range(6)),
                #             placeholder ="Select sample"
                #             ),
                #         html.Br()
                #         ]),
                #     ])
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
                                html.P("Select sex : "),
                                dcc.Dropdown(
                                    id="select_sex_attention_video_2",
                                    options=[{"value": 0, "label": "Female"}, {"value": 1, "label": "Male"}],
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
                                    id="select_age_group_attention_video_2",
                                    options=get_dataset_options(["Young", "Middle", "Old"]),
                                    placeholder="Select an age group : ",
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
                                html.P("Select an aging rate : "),
                                dcc.Dropdown(
                                    id="select_aging_rate_attention_video_2",
                                    options=get_dataset_options(["Decelerated", "Normal", "Accelerated"]),
                                    placeholder="Select an aging rate",
                                ),
                                html.Br(),
                            ]
                        ),
                    ]
                ),
                # dbc.Col([
                #     dbc.FormGroup([
                #         html.P("Select sample : "),
                #         dcc.Dropdown(
                #             id = 'select_sample_attention_video_2',
                #             options = get_dataset_options(range(6)),
                #             placeholder ="Select sample"
                #             ),
                #         html.Br()
                #         ]),
                #     ])
            ]
        )
    ]
)

layout = dbc.Container(
    [
        html.H1("AttentionMaps - Videos"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([controls, html.Br(), html.Br()], md=3),
                dbc.Col(
                    [
                        html.H3(id="score_videos"),
                        controls_1,
                        dcc.Loading(id="gif_display_1"),
                        controls_2,
                        dcc.Loading(id="gif_display_2"),
                    ],
                    style={"overflowX": "scroll", "width": 1000},
                    md=9,
                ),
            ]
        ),
    ],
    fluid=True,
)


@app.callback(
    Output("score_videos", "children"),
    [
        Input("select_organ_attention_video", "value"),
        Input("select_view_attention_video", "value"),
        Input("select_transformation_attention_video", "value"),
    ],
)
def generate_score(organ, view, transformation):
    if None not in [organ, view, transformation]:
        score_model = score[
            (score["organ"] == organ) & (score["view"] == view) & (score["transformation"] == transformation)
        ][["architecture", "R-Squared_all", "N_all"]]
        best_row = score_model.sort_values("R-Squared_all", ascending=False).iloc[0]
        title = "R2 = %.3f (%s), " % (best_row["R-Squared_all"], best_row["architecture"])
        title += "Sample size = %d" % best_row["N_all"]

        ## Old title
        # score_model = score_model.sort_values('R-Squared_all').iloc[0]
        # title = 'Best R-Squared :  %.3f, Sample Size %d' % (score_model['R-Squared_all'], score_model['N_all'])
        return title
    else:
        return ""


@app.callback(
    Output("gif_display_1", "children"),
    [
        Input("select_organ_attention_video", "value"),
        Input("select_view_attention_video", "value"),
        Input("select_transformation_attention_video", "value"),
        Input("select_sex_attention_video_1", "value"),
        Input("select_age_group_attention_video_1", "value"),
        Input("select_aging_rate_attention_video_1", "value"),
        # Input('select_sample_attention_video_1', 'value')
    ],
)
def _display_gif(organ, view, transformation, sex, age_group, aging_rate):  # , sample):
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:  # , sample]:
        df = load_csv(
            path_attention_maps_videos + "AttentionMaps-samples_Age_%s_%s_%s.csv" % (organ, view, transformation)
        )
        df = df[(df.Sex == sex) & (df.age_category == age_group.lower()) & (df.aging_rate == aging_rate.lower())]
        eid = df.iloc[sample].eid
        age = df.iloc[sample].Age
        res = df.iloc[sample].res
        title = "Chronological Age = %.3f, Biological Age = %.3f" % (age, age + res)
        path_to_gif = df.iloc[sample].Gif.split("/")[-1]
        path_to_gif = path_gif + path_to_gif
        path_to_jpg = df.iloc[sample].Picture.split("/")[-1]
        path_to_jpg = path_img + path_to_jpg
        print(app.get_asset_url(path_to_gif))
        gif_display = html.Div(
            [html.H3(title), gif.GifPlayer(gif=app.get_asset_url(path_to_gif), still=app.get_asset_url(path_to_jpg))]
        )
        return gif_display
    else:
        return dcc.Graph(figure=Figure(empty_graph))


@app.callback(
    Output("gif_display_2", "children"),
    [
        Input("select_organ_attention_video", "value"),
        Input("select_view_attention_video", "value"),
        Input("select_transformation_attention_video", "value"),
        Input("select_sex_attention_video_2", "value"),
        Input("select_age_group_attention_video_2", "value"),
        Input("select_aging_rate_attention_video_2", "value"),
        # Input('select_sample_attention_video_2', 'value')
    ],
)
def _display_gif(organ, view, transformation, sex, age_group, aging_rate):  # , sample):
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:  # , sample]:
        df = load_csv(
            path_attention_maps_videos + "AttentionMaps-samples_Age_%s_%s_%s.csv" % (organ, view, transformation)
        )
        df = df[(df.Sex == sex) & (df.age_category == age_group.lower()) & (df.aging_rate == aging_rate.lower())]
        eid = df.iloc[sample].eid
        age = df.iloc[sample].Age
        res = df.iloc[sample].res
        title = "Chronological Age = %.3f, Biological Age = %.3f" % (age, age + res)
        path_to_gif = df.iloc[sample].Gif.split("/")[-1]
        path_to_gif = path_gif + path_to_gif
        path_to_jpg = df.iloc[sample].Picture.split("/")[-1]
        path_to_jpg = path_img + path_to_jpg
        gif_display = html.Div(
            [html.H3(title), gif.GifPlayer(gif=app.get_asset_url(path_to_gif), still=app.get_asset_url(path_to_jpg))]
        )
        return gif_display
    else:
        return dcc.Graph(figure=Figure(empty_graph))
