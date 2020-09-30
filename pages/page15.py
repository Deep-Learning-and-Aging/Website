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
path_attention_maps_metadata = './' + app.get_asset_url('page9_AttentionMaps/Attention_maps_infos/')
path_img = './' + app.get_asset_url('page15_AttentionMapsTimeSeries/img/Age')
aging_rate = 'Normal'
controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_time',
            options = get_dataset_options(['Arterial', 'Heart', 'PhysicalActivity']),
            placeholder ="Select an organ"
            ),
            html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_time',
            options = [],
            placeholder ="Select a view"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_time',
            options = [],
            placeholder = "Select a transformation"
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select channel : "),
        dcc.Dropdown(
            id = 'select_time_channel',
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
                id = 'select_sex_time_1',
                options = get_dataset_options(['Male', 'Female']),
                placeholder ="Select a sex"
                ),
            html.Br()
            ])
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_time_1',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
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
                id = 'select_sex_time_2',
                options = get_dataset_options(['Male', 'Female']),
                placeholder ="Select a sex"
                ),
            html.Br()
            ])
        ]),
    dbc.Col([
        dbc.FormGroup([
            html.P("Select an age group : "),
            dcc.Dropdown(
                id = 'select_age_group_time_2',
                options = get_dataset_options(['Young', 'Middle', 'Old']),
                placeholder ="Select an age group : "
                ),
            html.Br()
            ]),
        ])
    ])

layout = dbc.Container([
                html.H1('Datasets - TimeSeries'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [controls_1,
                        dcc.Graph(id = 'timeseries_raw_display_1'),
                        controls_2,
                        dcc.Graph(id = 'timeseries_raw_display_2'),
                        ],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ])
            ], fluid = True)

@app.callback(Output('select_view_time', 'options'),
             [Input('select_organ_time', 'value')])
def _get_options_transformation(value_organ):
    if value_organ == 'Arterial':
        return get_dataset_options(['PulseWaveAnalysis'])
    elif value_organ == 'Heart':
        return get_dataset_options(['ECG'])
    elif value_organ == 'PhysicalActivity':
        return get_dataset_options(['FullWeek', 'Walking'])
    else :
        return []

@app.callback(Output('select_time', 'options'),
             [Input('select_view_time', 'value'), Input('select_transformation_time', 'value')])
def _get_options_transformation(value_view, value_transformation):
    if value_view == 'PulseWaveAnalysis':
        return get_dataset_options([str(elem) for elem in range(1, 1+1)])
    elif value_view == 'ECG':
        return get_dataset_options([str(elem) for elem in range(1, 12 + 1)])
    elif value_view == 'FullWeek':
        if value_transformation == 'Acceleration':
            return get_dataset_options([str(elem) for elem in range(1, 1 + 1)])
        elif value_transformation == 'TimeSeriesFeatures' :
            return get_dataset_options([str(elem) for elem in range(1, 113 + 1)])
    elif value_view == 'Walking':
        return get_dataset_options([str(elem) for elem in range(1, 3 + 1)])
    else :
        return []

@app.callback(Output('select_transformation_time', 'options'),
             [Input('select_view_time', 'value')])
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


@app.callback(Output('timeseries_raw_display_1', 'figure'),
             [Input('select_organ_time', 'value'),
              Input('select_view_time', 'value'),
              Input('select_transformation_time', 'value'),
              Input('select_sex_time_1', 'value'),
              Input('select_age_group_time_1', 'value'),
              Input('select_time_channel', 'value')
             ])
def _display_gif(organ, view, transformation, sex, age_group, channel):
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:
        channel = int(channel)
        path_metadata = path_attention_maps_metadata + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation)
        df_metadata = pd.read_csv(path_metadata)
        df_metadata =  df_metadata[(df_metadata.sex == sex) & (df_metadata.age_category == age_group.lower()) & (df_metadata.aging_rate == aging_rate.lower()) & (df_metadata['sample'] == channel)]
        path_raw = path_img + '%s/%s/%s/%s/%s/%s/Saliency_Age_%s_%s_%s_%s_%s_%s_0.npy' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower(),organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
        numpy_arr_raw = np.load(path_raw)
        if view == 'ECG' :
            unit_x = '2ms/Lsb'
            unit_y = '5uV/Lsb'
        elif view == 'PulseWaveAnalysis':
            unit_x = '10ms/Lsb'
            unit_y = 'blood-pressure [normalized]'
        elif view == 'Walking':
            unit_x == '10ms/Lsb'
            unit_y == 'milligravity'
        elif view == 'FullWeek':
            if transformation == 'Acceleration' :
                unit_x = '1min/Lsb'
                unit_y = 'milligravity'
            elif transformation == 'TimeSeriesFeatures' :
                unit_x = '5min/Lsb'
                unit_y = 'NONE'
            else :
                unit_x = ''
                unit_y = ''
        else :
            unit_x = ''
            unit_y = ''

        np_channel = numpy_arr_raw[channel - 1]
        scatter = go.Scatter(
            y = np_channel,
            mode='markers',
            marker=dict(
                size=5
                )
            )
        d = {'data' : [scatter], 'layout' : {'xaxis' : {'title' : {'text' : unit_x}},
                                             'yaxis' : {'title' : {'text' : unit_y}}}
            }
        return go.Figure(d)
    else :
        return go.Figure(empty_graph)
        #print(numpy_arr_raw,numpy_arr_raw.shape,  numpy_attentionmap, numpy_attentionmap.shape)
@app.callback(Output('timeseries_raw_display_2', 'figure'),
             [Input('select_organ_time', 'value'),
              Input('select_view_time', 'value'),
              Input('select_transformation_time', 'value'),
              Input('select_sex_time_2', 'value'),
              Input('select_age_group_time_2', 'value'),
              Input('select_time_channel', 'value')
             ])
def _display_gif2(organ, view, transformation, sex, age_group, channel):
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:
        path_raw = path_img + '%s/%s/%s/%s/%s/%s/Saliency_Age_%s_%s_%s_%s_%s_%s_0.npy' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower(),organ, view, transformation, sex, age_group.lower(), aging_rate.lower())
        numpy_arr_raw = np.load(path_raw)
        if view == 'ECG' :
            unit_x = '2ms/Lsb'
            unit_y = '5uV/Lsb'
        elif view == 'PulseWaveAnalysis':
            unit_x = '10ms/Lsb'
            unit_y = 'blood-pressure [normalized]'
        elif view == 'Walking':
            unit_x == '10ms/Lsb'
            unit_y == 'milligravity'
        elif view == 'FullWeek':
            if transformation == 'Acceleration' :
                unit_x = '1min/Lsb'
                unit_y = 'milligravity'
            elif transformation == 'TimeSeriesFeatures' :
                unit_x = '5min/Lsb'
                unit_y = 'NONE'
            else :
                unit_x = ''
                unit_y = ''
        else :
            unit_x = ''
            unit_y = ''
        channel = int(channel)
        np_channel = numpy_arr_raw[channel - 1]
        scatter = go.Scatter(
            y = np_channel,
            mode='markers',
            marker=dict(
                size=5
                )
            )
        d = {'data' : [scatter], 'layout' : {'xaxis' : {'title' : {'text' : unit_x}},
                                             'yaxis' : {'title' : {'text' : unit_y}}}
            }
        return go.Figure(d)
    else :
        return go.Figure(empty_graph)
