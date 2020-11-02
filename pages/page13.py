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

path_attention_maps = './' + app.get_asset_url('page9_AttentionMaps/Images/Age/')
path_attention_maps_infos = './' + app.get_asset_url('page9_AttentionMaps/Attention_maps_infos/AttentionMaps-samples_Age_')
controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_attention_time',
            options = get_dataset_options(['Arterial', 'Heart', 'PhysicalActivity']),
            placeholder ="Select an organ"
            ),
            html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_attention_time',
            options = [],
            placeholder ="Select a view"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_attention_time',
            options = [],
            placeholder = "Select a transformation"
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select channel : "),
        dcc.Dropdown(
            id = 'select_channel_time',
            options = get_dataset_options(['1']),
            placeholder ="Select which channel to display",
            value= '1'
        ),
        html.Br()
        ]),
    ])

controls_1 = dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            html.P("Select sex : "),
            dcc.Dropdown(
                id = 'select_sex_attention_time_1',
                options = get_dataset_options(['Male', 'Female']),
                placeholder ="Select a sex"
                ),
            html.Br()
            ]),
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_attention_time_1',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
                ),
            html.Br()
            ]),
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an aging rate : "),
            dcc.Dropdown(
                id = 'select_aging_rate_attention_time_1',
                options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
                placeholder ="Select an aging rate"
                ),
            html.Br()
        ]),
    ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select sample : "),
            dcc.Dropdown(
                id = 'select_sample_attention_time_1',
                options = get_dataset_options([i for i in range(10)]),
                placeholder ="Select sample"
                ),
            html.Br()
        ]),
    ])
])

controls_2 = dbc.Row([
    dbc.Col([
        dbc.FormGroup([
            html.P("Select sex : "),
            dcc.Dropdown(
                id = 'select_sex_attention_time_2',
                options = get_dataset_options(['Male', 'Female']),
                placeholder ="Select a sex"
                ),
            html.Br()
            ]),
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_attention_time_2',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
                ),
            html.Br()
            ]),
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an aging rate : "),
            dcc.Dropdown(
                id = 'select_aging_rate_attention_time_2',
                options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
                placeholder ="Select an aging rate"
                ),
            html.Br()
            ]),
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select sample : "),
            dcc.Dropdown(
                id = 'select_sample_attention_time_2',
                options = get_dataset_options([i for i in range(10)]),
                placeholder ="Select sample"
                ),
            html.Br()
        ]),
    ])
])

layout = dbc.Container([
                html.H1('AttentionMaps - Time Series'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [controls_1,
                        html.H3(id = 'title_timeseries_1'),
                        dcc.Graph(id = 'timeseries_display_1'),
                        controls_2,
                        html.H3(id = 'title_timeseries_2'),
                        dcc.Graph(id = 'timeseries_display_2')],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ])
            ], fluid = True)

@app.callback(Output('select_view_attention_time', 'options'),
             [Input('select_organ_attention_time', 'value')])
def _get_options_transformation(value_organ):
    if value_organ == 'Arterial':
        return get_dataset_options(['PulseWaveAnalysis'])
    elif value_organ == 'Heart':
        return get_dataset_options(['ECG'])
    elif value_organ == 'PhysicalActivity':
        return get_dataset_options(['FullWeek', 'Walking'])
    else :
        return []

@app.callback(Output('select_channel_time', 'options'),
             [Input('select_view_attention_time', 'value'), Input('select_transformation_attention_time', 'value')])
def _get_options_transformation(value_view, value_transformation):
    if value_view == 'PulseWaveAnalysis':
        return get_dataset_options([str(elem) for elem in range(1, 1+1)])
    elif value_view == 'ECG':
        return get_dataset_options([str(elem) for elem in range(1, 15 + 1)])
    elif value_view == 'FullWeek':
        if value_transformation == 'Acceleration':
            return get_dataset_options([str(elem) for elem in range(1, 1 + 1)])
        elif value_transformation == 'TimeSeriesFeatures' :
            return get_dataset_options([str(elem) for elem in range(1, 113 + 1)])
    elif value_view == 'Walking':
        return get_dataset_options([str(elem) for elem in range(1, 3 + 1)])
    else :
        return []

@app.callback(Output('select_transformation_attention_time', 'options'),
             [Input('select_view_attention_time', 'value')])
def _get_options_transformation(value_view):
    if value_view == 'PulseWaveAnalysis' or value_view == 'ECG':
        print(get_dataset_options(['TimeSeries']))
        return get_dataset_options(['TimeSeries'])
    elif value_view == 'FullWeek':
        return get_dataset_options(['Acceleration', 'TimeSeriesFeatures'])
    elif value_view == 'Walking':
        return get_dataset_options(['3D'])
    else :
        return []


@app.callback([Output('timeseries_display_1', 'figure'),
               Output('title_timeseries_1', 'children')],
             [Input('select_organ_attention_time', 'value'),
              Input('select_view_attention_time', 'value'),
              Input('select_transformation_attention_time', 'value'),
              Input('select_sex_attention_time_1', 'value'),
              Input('select_age_group_attention_time_1', 'value'),
              Input('select_aging_rate_attention_time_1', 'value'),
              Input('select_channel_time', 'value'),
              Input('select_sample_attention_time_1', 'value')
             ])
def _display_gif(organ, view, transformation, sex, age_group, aging_rate, channel, sample):
    if None not in [organ, view, transformation, sex, age_group, aging_rate, sample]:
        df = pd.read_csv(path_attention_maps_infos + organ + '_' + view + '_' + transformation + '.csv')
        df = df[(df['sex'] == sex) & (df['age_category'] == age_group.lower()) & (df['aging_rate'] == aging_rate.lower()) & (df['sample'] == sample)]
        df_bioage = df['Biological_Age']
        df_chroage = df['Age']
        title = 'Chronological Age = %.3f, Biological Age = %.3f' % (df_chroage, df_bioage)
        path_attentionmaps = path_attention_maps + '%s/%s/%s/%s/%s/%s/Saliency_Age_%s_%s_%s_%s_%s_%s_%s.npy' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower(),organ, view, transformation, sex, age_group.lower(), aging_rate.lower(), sample)
        numpy_attentionmap = np.load(path_attentionmaps)
        channel = int(channel)
        np_channel = numpy_attentionmap[channel-1, :, :]
        np_channel_data = np_channel[0]
        np_channel_couleur = np_channel[1]
        scatter = go.Scatter(
            y = np_channel_data,
            mode='markers',
            marker=dict(
                size=5,
                color=np_channel_couleur, #set color equal to a variable
                colorscale='RdBu_r', # one of plotly colorscales
                showscale=True
                )
            )
        d = {'data' : [scatter]}
        return go.Figure(d), title
    else :
        return go.Figure(empty_graph), ''

@app.callback([Output('timeseries_display_2', 'figure'),
               Output('title_timeseries_2', 'children')],
             [Input('select_organ_attention_time', 'value'),
              Input('select_view_attention_time', 'value'),
              Input('select_transformation_attention_time', 'value'),
              Input('select_sex_attention_time_2', 'value'),
              Input('select_age_group_attention_time_2', 'value'),
              Input('select_aging_rate_attention_time_2', 'value'),
              Input('select_channel_time', 'value'),
              Input('select_sample_attention_time_2', 'value')
             ])
def _display_gif(organ, view, transformation, sex, age_group, aging_rate, channel, sample):
    if None not in [organ, view, transformation, sex, age_group, aging_rate, sample]:
        df = pd.read_csv(path_attention_maps_infos + organ + '_' + view + '_' + transformation + '.csv')
        df = df[(df['sex'] == sex) & (df['age_category'] == age_group.lower()) & (df['aging_rate'] == aging_rate.lower()) & (df['sample'] == sample)]
        df_bioage = df['Biological_Age']
        df_chroage = df['Age']
        title = 'Chronological Age = %.3f, Biological Age = %.3f' % (df_chroage, df_bioage)
        path_attentionmaps = path_attention_maps + '%s/%s/%s/%s/%s/%s/Saliency_Age_%s_%s_%s_%s_%s_%s_%s.npy' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower(),organ, view, transformation, sex, age_group.lower(), aging_rate.lower(), sample)
        numpy_attentionmap = np.load(path_attentionmaps)
        channel = int(channel)
        np_channel = numpy_attentionmap[channel-1, :, :]
        np_channel_data = np_channel[0]
        np_channel_couleur = np_channel[1]
        scatter = go.Scatter(
            y = np_channel_data,
            mode='markers',
            marker=dict(
                size=5,
                color=np_channel_couleur, #set color equal to a variable
                colorscale='RdBu_r', # one of plotly colorscales
                showscale=True
                )
            )
        d = {'data' : [scatter]}
        return go.Figure(d), title
    else :
        return go.Figure(empty_graph), ''
        #print(numpy_arr_raw,numpy_arr_raw.shape,  numpy_attentionmap, numpy_attentionmap.shape)
