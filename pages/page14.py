import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, dict_dataset_images_to_organ_and_view
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
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
aging_rate = 'Normal'
path_attention_maps = './' + app.get_asset_url('page9_AttentionMaps/Images/Age')

if MODE != 'All':
    organ_select = dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_image',
            options = get_dataset_options([MODE]),
            placeholder ="Select an organ",
            value = MODE
            ),
            html.Br()
        ], style = {'display' : 'None'})
else :
    organ_select = dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_image',
            options = get_dataset_options(dict_dataset_images_to_organ_and_view.keys()),
            placeholder ="Select an organ"
            ),
            html.Br()
        ])

controls = dbc.Card([
    organ_select,
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_image',
            options = get_dataset_options([]),
            placeholder ="Select a view"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_image',
            options = get_dataset_options([]),
            placeholder ="Select a transformation"
            ),
        html.Br()
        ]),
    ])

controls_2 = dbc.Card([
    dbc.FormGroup([
        html.P("Select Sex : "),
        dcc.Dropdown(
            id = 'select_sex_image',
            options = get_dataset_options(['Male', 'Female']),
            placeholder ="Select a sex"
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select an age group : "),
        dcc.Dropdown(
            id = 'select_age_group_image',
            options = get_dataset_options(['Young', 'Middle', 'Old']),
            placeholder ="Select an age group"
            ),
        html.Br()
        ]),
    # dbc.FormGroup([
    #     html.P("Select an aging rate : "),
    #     dcc.Dropdown(
    #         id = 'select_aging_rate_image',
    #         options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
    #         placeholder ="Select an aging rate"
    #         ),
    #     html.Br()
    #     ]),
])

@app.callback(Output('select_transformation_image', 'options'),
              [Input('select_organ_image', 'value'), Input('select_view_image', 'value')])
def generate_list_view_list(value_organ, value_view):
    if value_view is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value_organ][value_view])


@app.callback(Output('select_view_image', 'options'),
              [Input('select_organ_image', 'value')])
def generate_list_view_list(value):
    if value is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value])



layout =  html.Div([
        html.H1('Datasets - Images'),
        dbc.Container([
            dbc.Row(
                    children = [
                        dbc.Col([controls,
                                 html.Br(),
                                 controls_2,
                                 html.Br(),
                                 html.Br(),
                                 ], md=4),
                        dbc.Col(id = 'columns_image',
                            md=8)
                        ])
            ],
            style={"height": "100vh"},
            fluid = True)
        ]
    )


@app.callback(Output('columns_image', 'children'),
             [Input('select_organ_image', 'value'),
              Input('select_view_image', 'value'),
              Input('select_transformation_image', 'value'),
              Input('select_sex_image', 'value'),
              Input('select_age_group_image', 'value'),
              #Input('select_aging_rate_image', 'value')
              ])
def _plot_manhattan_plot(organ, view, transformation, sex, age_group):#, aging_rate):
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:
        if (organ, view) in [('Eyes','Fundus'), ('Eyes','OCT'), ('Arterial', 'Carotids'), ('Musculoskeletal', 'Knees'), ('Musculoskeletal', 'Hips')] :
            title = '# TO MODIFY : SELECT TITLE'
            path_image_left = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/left/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_left.jpg' % sample
            path_image_right = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/right/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_right.jpg' % sample
            raw_left = mpimg.imread(path_image_left)
            raw_right = mpimg.imread(path_image_right)

            raw_left = Image.fromarray((raw_left).astype(np.uint8)).convert('RGB')
            raw_right = Image.fromarray((raw_right).astype(np.uint8)).convert('RGB')

            buffered_left = BytesIO()
            raw_left.save(buffered_left, format="PNG")
            img_base64_left = base64.b64encode(buffered_left.getvalue()).decode('ascii')
            src_left = 'data:image/png;base64,{}'.format(img_base64_left)

            buffered_right = BytesIO()
            raw_right.save(buffered_right, format="PNG")
            img_base64_right = base64.b64encode(buffered_right.getvalue()).decode('ascii')
            src_right = 'data:image/png;base64,{}'.format(img_base64_right)
            col = [
                    html.H3(title),
                    html.Img(id = 'attentionmap_left', style={'height':'50%', 'width':'50%'},
                             src = src_left),
                    html.Img(id = 'attentionmap_right', style={'height':'50%', 'width':'50%'},
                             src = src_right)
                 ]
            return col

        else :
            title = '# TO MODIFY : SELECT TITLE'
            path_image = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group, aging_rate) + 'RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group + '_' + aging_rate + '_%s.jpg' % sample
            raw = mpimg.imread(path_image)
            raw = Image.fromarray((raw).astype(np.uint8)).convert('RGB')
            buffered = BytesIO()
            raw.save(buffered, format="PNG")
            img_base64 = base64.b64encode(buffered.getvalue()).decode('ascii')
            src = 'data:image/png;base64,{}'.format(img_base64)
            col = [
                    html.H3(title),
                    html.Img(id = 'attentionmap', style={'height':'50%', 'width':'50%'},
                                src = src),
                ]
            return col
    else :
        return []
