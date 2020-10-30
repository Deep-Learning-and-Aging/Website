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
sample = 0
path_gif = 'page12_AttentionMapsVideos/RawVideos/MRI/'
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
            options = get_dataset_options(['3chambersRawVideo', '4chambersRawVideo']),
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

        #title = 'Chronological Age = %.3f, Biological Age = %.3f' % (age, age + res)
        path_to_gif = path_gif + '%s/%s/%s/RawVideo_Age_Heart_MRI_%s_%s_%s_%s.' % (transformation, dict_sex_id_to_sex[sex], age_group.lower(), transformation, dict_sex_id_to_sex[sex], age_group.lower(), sample)
        path_to_gif_img = path_to_gif + 'gif'
        path_to_jpg_img = path_to_gif + 'png'
        print(path_to_gif)
        frame = Image.open('./' + app.get_asset_url(path_to_gif_img))
        frame.seek(0)
        print(frame)
        frame.save('./' + app.get_asset_url(path_to_jpg_img))
        gif_display = html.Div([
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif_img),
                still = app.get_asset_url(path_to_jpg_img)
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

        #title = 'Chronological Age = %.3f, Biological Age = %.3f' % (age, age + res)
        path_to_gif = path_gif + '%s/%s/%s/RawVideo_Age_Heart_MRI_%s_%s_%s_%s.' % (transformation, dict_sex_id_to_sex[sex], age_group.lower(), transformation, dict_sex_id_to_sex[sex], age_group.lower(), sample)
        path_to_gif_img = path_to_gif + 'gif'
        path_to_jpg_img = path_to_gif + 'png'
        print(path_to_gif)
        frame = Image.open('./' + app.get_asset_url(path_to_gif_img))
        frame.seek(0)
        print(frame)
        frame.save('./' + app.get_asset_url(path_to_jpg_img))
        gif_display = html.Div([
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif_img),
                still = app.get_asset_url(path_to_jpg_img)
            )])
        return gif_display
    else :
        return dcc.Graph(figure = go.Figure(empty_graph))
