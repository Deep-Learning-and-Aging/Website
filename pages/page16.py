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
path_gif = 'page12_AttentionMapsVideos/RawVideos/MRI/'
path_attention_maps_videos = 'page12_AttentionMapsVideos/AttentionMapsVideos/'
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
    dbc.Button("Reset", id = 'reset_page16', className="mr-2", color = "primary"),
    ])

@app.callback([Output("select_organ_attention_video_raw", "value"),
               Output("select_view_attention_video_raw", "value"),
               Output("select_transformation_attention_video_raw", "value")],
               [Input("reset_page16", "n_clicks")])
def reset(n):
    if n :
        if n > 0 :
            return [None, None, None]
    else :
        raise PreventUpdate()



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
    dbc.Col([
        dbc.FormGroup([
            html.P("Select a sample : "),
            dcc.Dropdown(
                id = 'select_sample_attention_video_1_raw',
                options = get_dataset_options(range(10)),
                placeholder ="Select a sample: "
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
    ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select a sample : "),
            dcc.Dropdown(
                id = 'select_sample_attention_video_2_raw',
                options = get_dataset_options(range(10)),
                placeholder ="Select a sample: "
                ),
            html.Br()
            ]),
        ]),
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
                        html.H3(id = 'title_video_raw1'),
                        dcc.Loading(id = 'gif_display_1_raw'),
                        controls_2,
                        html.H3(id = 'title_video_raw2'),
                        dcc.Loading(id = 'gif_display_2_raw')],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ])
            ], fluid = True)

@app.callback([Output('gif_display_1_raw', 'children'),
               Output('title_video_raw1', 'children')],
             [Input('select_organ_attention_video_raw', 'value'),
              Input('select_view_attention_video_raw', 'value'),
              Input('select_transformation_attention_video_raw', 'value'),
              Input('select_sex_attention_video_1_raw', 'value'),
              Input('select_age_group_attention_video_1_raw', 'value'),
              Input('select_sample_attention_video_1_raw', 'value')
             ])
def _display_gif(organ, view, transformation, sex, age_group, sample):
    if None not in [organ, view, transformation, sex, age_group, sample]:
        df = load_csv('page12_AttentionMapsVideos/RawVideos/files/' + 'AttentionMaps-samples_Age_Heart_MRI_%s.csv' % transformation)
        df = df[(df['age_category'] == age_group.lower()) & (df['Sex'] == sex) & (df['sample'] == int(sample)) & (df['aging_rate'] == 'normal')]
        title = 'Chronological Age = %.3f' % df['Age']
        path_to_gif = path_gif + '%s/%s/%s/RawVideo_Age_Heart_MRI_%s_%s_%s_%s.' % (transformation, dict_sex_id_to_sex[sex], age_group.lower(), transformation, dict_sex_id_to_sex[sex], age_group.lower(), sample)
        path_to_gif_img = path_to_gif + 'gif'
        path_to_jpg_img = path_to_gif + 'png'
        #frame = Image.open('./' + app.get_asset_url(path_to_gif_img))
        #frame.seek(0)
        #frame.save('./' + app.get_asset_url(path_to_jpg_img))
        gif_display = html.Div([
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif_img),
                still = app.get_asset_url(path_to_jpg_img)
            )])
        return gif_display, title
    else :
        return dcc.Graph(figure = Figure(empty_graph)), ''

@app.callback([Output('gif_display_2_raw', 'children'),
               Output('title_video_raw2', 'children')],
             [Input('select_organ_attention_video_raw', 'value'),
              Input('select_view_attention_video_raw', 'value'),
              Input('select_transformation_attention_video_raw', 'value'),
              Input('select_sex_attention_video_2_raw', 'value'),
              Input('select_age_group_attention_video_2_raw', 'value'),
               Input('select_sample_attention_video_2_raw', 'value')
             ])
def _display_gif(organ, view, transformation, sex, age_group, sample):
    if None not in [organ, view, transformation, sex, age_group, sample]:
        df = load_csv('page12_AttentionMapsVideos/RawVideos/files/' + 'AttentionMaps-samples_Age_Heart_MRI_%s.csv' % transformation)
        df = df[(df['age_category'] == age_group.lower()) & (df['Sex'] == sex) & (df['sample'] == int(sample)) & (df['aging_rate'] == 'normal')]
        title = 'Chronological Age = %.3f' % df['Age']
        path_to_gif = path_gif + '%s/%s/%s/RawVideo_Age_Heart_MRI_%s_%s_%s_%s.' % (transformation, dict_sex_id_to_sex[sex], age_group.lower(), transformation, dict_sex_id_to_sex[sex], age_group.lower(), sample)
        path_to_gif_img = path_to_gif + 'gif'
        path_to_jpg_img = path_to_gif + 'png'
        #frame = Image.open('./' + app.get_asset_url(path_to_gif_img))
        #frame.seek(0)
        #frame.save('./' + app.get_asset_url(path_to_jpg_img))
        gif_display = html.Div([
            gif.GifPlayer(
                gif = app.get_asset_url(path_to_gif_img),
                still = app.get_asset_url(path_to_jpg_img)
            )])
        return gif_display, title
    else :
        return dcc.Graph(figure = Figure(empty_graph)), ''
