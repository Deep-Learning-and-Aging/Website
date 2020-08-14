import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from app import app, MODE, filename
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64

organs_gwas = ['Heart', 'Liver']
if MODE != 'All':
    style = {'display' : 'None'}
    value = MODE
    organs_gwas = [MODE]
else :
    style = {}
    value = organs_gwas[0]

path_attention_maps = filename + 'page9_AttentionMaps/AttentionMaps/AttentionMap_'


controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select an organ: "),
        dcc.Dropdown(
            id='select_organ_map',
            options = get_dataset_options(organs_gwas),
            value = value
            ),
        html.Br()
    ])
], style = style)


layout =  html.Div([
        html.H1('Images - Attention Maps'),
        dbc.Container([
            dbc.Row([
                dbc.Col([controls,
                         html.Br(),
                         html.Br(),
                         ], md=4),
                dbc.Col(
                    [
                        html.Img(id = 'attentionmap', style={'height':'50%', 'width':'50%'})
                     ],
                    md=8)
                ])
            ],
            style={"height": "100vh"},
            fluid = True)
        ]
    )



@app.callback(Output('attentionmap', 'src'),
             [Input('select_organ_map', 'value')])
def _plot_manhattan_plot(organ):
    if organ is not None:
        path_png = path_attention_maps + organ + '.png'
        img_base64 = base64.b64encode(open(path_png, 'rb').read()).decode('ascii')
        src = 'data:image/png;base64,{}'.format(img_base64)
        return src
    else :
        return ''
