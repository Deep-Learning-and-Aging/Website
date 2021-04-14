import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, load_csv
import pandas as pd
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
import plotly.express as px

from dash_website.app import APP, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64


filename_heritabilty = "page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv"
df = load_csv(filename_heritabilty)
organs_gwas = df["Organ"].drop_duplicates()
if MODE != "All":
    style = {"display": "None"}
    value = MODE
else:
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
d["data"] = Bar(x=df["Organ"], y=df["h2"], error_y=dict(type="data", array=df["h2_sd"]), name="Heritability")
d["layout"] = {
    "yaxis": {"title": {"text": "Heritability"}},
    "height": 700
    #'yaxis' : {'title' : {'text' : unit_y}}
}
figure = Figure(d)

layout = dbc.Container(
    [
        html.H1("Genetics - Heritability"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Graph(id="Plot Heritability", figure=figure),
                    ],
                    style={"overflowX": "scroll", "width": 800},
                    md=9,
                )
            ]
        ),
    ],
    fluid=True,
)