import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output
from .tools import get_dataset_options, empty_graph
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

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

path_gif = 'page12_AttentionMapsVideos/RawVideos/MRI'
path_attention_maps_videos = './' + app.get_asset_url('page12_AttentionMapsVideos/AttentionMapsVideos/')
controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_attention_video_raw',
            options = get_dataset_options(['Heart']),
            placeholder ="Select an organ",
            value = 'Heart'
            ),
            html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_attention_video_raw',
            options = get_dataset_options(['MRI']),
            placeholder ="Select a view",
            value = 'MRI'
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_attention_video_raw',
            options = get_dataset_options(['3chambersRaw', '4chambersRaw']),
            placeholder ="Select a transformation"
            ),
        html.Br()
        ]),
    ])

controls_1  =  dbc.Card([
dbc.Row([
    dbc.Col([
    dbc.FormGroup([
        html.P("Select sex : "),
        dcc.Dropdown(
            id = 'select_sex_attention_video_1_raw',
            options = [{'value' : 0, 'label' : 'Female'}, {'value' : 1, 'label' : 'Male'}],
            placeholder ="Select a sex"
            ),
        html.Br()
        ]),
    ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_attention_video_1_raw',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
                ),
            html.Br()
            ]),
        ]),
    ])
])
controls_2  =  dbc.Card([
dbc.Row([
    dbc.Col([
    dbc.FormGroup([
        html.P("Select sex : "),
        dcc.Dropdown(
            id = 'select_sex_attention_video_2_raw',
            options = [{'value' : 0, 'label' : 'Female'}, {'value' : 1, 'label' : 'Male'}],
            placeholder ="Select a sex"
            ),
        html.Br()
        ]),
    ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_attention_video_2_raw',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
                ),
            html.Br()
            ]),
        ]),
    ])
])
dict_sex_id_to_sex = {0 : 'Female', 1 : 'Male'}

layout = dbc.Container([
                html.H1('Datasets - Videos'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [controls_1,
                        dcc.Loading(id = 'gif_display_1_raw'),
                        controls_2,
                        dcc.Loading(id = 'gif_display_2_raw')],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ])
            ], fluid = True)

@app.callback(Output('gif_display_1_raw', 'children'),
             [Input('select_organ_attention_video_raw', 'value'),
              Input('select_view_attention_video_raw', 'value'),
              Input('select_transformation_attention_video_raw', 'value'),
              Input('select_sex_attention_video_1_raw', 'value'),
              Input('select_age_group_attention_video_1_raw', 'value'),
             ])
def _display_gif(organ, view, transformation, sex, age_group):
    if None not in [organ, view, transformation, sex, age_group]:
        df = pd.read_csv(path_attention_maps_videos + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation))
        df = df[(df.Sex == sex) & (df.age_category == age_group.lower())]
        eid = df.iloc[0].eid
        age = df.iloc[0].Age
        res = df.iloc[0].res
        title = 'Chronological Age = %.3f, Biological Age = %.3f' % (age, age + res)
        path_to_gif = df.iloc[0].Gif.split('/')[-1]
        print(path_to_gif)
        path_to_gif = path_gif + path_to_gif
        path_to_jpg = df.iloc[0].Picture.split('/')[-1]
        path_to_jpg = path_gif + path_to_jpg
        gif_display = html.Div([
            html.H3(title),
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif),
                still = app.get_asset_url(path_to_jpg)
            )])
        return gif_display
    else :
        return dcc.Graph(figure = go.Figure(empty_graph))

@app.callback(Output('gif_display_2_raw', 'children'),
             [Input('select_organ_attention_video_raw', 'value'),
              Input('select_view_attention_video_raw', 'value'),
              Input('select_transformation_attention_video_raw', 'value'),
              Input('select_sex_attention_video_2_raw', 'value'),
              Input('select_age_group_attention_video_2_raw', 'value'),
             ])
def _display_gif(organ, view, transformation, sex, age_group):
    if None not in [organ, view, transformation, sex, age_group]:
        print(organ, view, transformation, sex, age_group)
        df = pd.read_csv(path_attention_maps_videos + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation))
        df = df[(df.Sex == sex) & (df.age_category == age_group.lower())]
        eid = df.iloc[0].eid
        age = df.iloc[0].Age
        res = df.iloc[0].res
        title = 'Chronological Age = %.3f, Biological Age = %.3f' % (age, age + res)
        path_to_gif = '%s/%s/%s/RawVideo_Age_Heart_MRI_%s_%s_%s_0.gif' % (transformation, dict_sex_id_to_sex[sex], age_group.lower(), transformation, dict_sex_id_to_sex[sex], age_group.lower())
        print(path_to_gif)
        path_to_gif = path_gif + path_to_gif
        gif_display = html.Div([
            html.H3(title),
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif),
            )])
        return gif_display
    else :
        return dcc.Graph(figure = go.Figure(empty_graph))
