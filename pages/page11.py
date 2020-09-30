import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale
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


filename_heritabilty = './' + app.get_asset_url('page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv')
df = pd.read_csv(filename_heritabilty)
organs_gwas = df['Organ'].drop_duplicates()
if MODE != 'All' :
    style = {'display' : 'None'}
    value = MODE
else :
    style = {}
    value = organs_gwas[0]

# controls1 = dbc.Card([
#     dbc.FormGroup([
#         html.P("Select an organ: "),
#         dcc.Dropdown(
#             id='select_organ',
#             options = get_dataset_options(organs_gwas),
#             value = value
#             ),
#         html.Br()
#     ])
# ], style = style)
#
# controls2 = dbc.Card([
#     dbc.FormGroup([
#         html.P("Select an organ: "),
#         dcc.Dropdown(
#             id='select_organ2',
#             options = get_dataset_options(organs_gwas),
#             value = value
#             ),
#         html.Br()
#     ])
# ], style = style)

d = dict()
d['data'] = go.Bar(
    x=df['Organ'],
    y=df['h2'],
    error_y = dict(type = 'data', array = df['h2_sd']),
    name='Heritability'
)
d['layout'] = {'xaxis' : {'title' : {'text' : 'Heritability'}},
               #'yaxis' : {'title' : {'text' : unit_y}}
               }
figure = go.Figure(d)

layout = dbc.Container([
                html.H1('Heritability Scores'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [dcc.Graph(
                             id='Plot Heritability',
                             figure = figure
                             ),
                         ],
                        style={'overflowY': 'scroll', 'height': 600, 'overflowX': 'scroll', 'width' : 700},
                         md=9)
                        ])
            ], fluid = True)
