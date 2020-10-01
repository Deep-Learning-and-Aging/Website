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

## Set performance file
performances = './' + app.get_asset_url('page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_eids_Age_test.csv')
df_perf = pd.read_csv(performances).set_index('version')
scores_organs = [elem.split('_')[1] for elem in df_perf.index.values]
scores_view = [(elem.split('_')[2]).replace('*', '').replace('HearingTest', '').replace('BloodCount', '') for elem in df_perf.index.values]
df_perf.index = [organ + view for organ, view in zip(scores_organs, scores_view)]
df_perf = df_perf['R-Squared_all']

## Set heritability file
filename_heritabilty = './' + app.get_asset_url('page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv')
df_heritability = pd.read_csv(filename_heritabilty).set_index('Organ')['h2']

filename_gwas_corr = './' + app.get_asset_url('page17_GWASCorrelations/')
corr_gwas = pd.read_csv(filename_gwas_corr + 'GWAS_correlations_Age.csv').set_index('Unnamed: 0')
corr_gwas_sd = pd.read_csv(filename_gwas_corr + 'GWAS_correlations_sd_Age.csv').set_index('Unnamed: 0')


if MODE != 'All' :
    corr_gwas = corr_gwas[corr_gwas.columns[corr_gwas.columns.str.contains(MODE)]]
    corr_gwas = corr_gwas.loc[corr_gwas.index.str.contains(MODE)]
    corr_gwas_sd = corr_gwas_sd[corr_gwas_sd.columns[corr_gwas_sd.columns.str.contains(MODE)]]
    corr_gwas_sd = corr_gwas_sd.loc[corr_gwas_sd.index.str.contains(MODE)]

intersection = df_perf.index.intersection(corr_gwas.index).intersection(df_heritability.index)
corr_gwas = corr_gwas[corr_gwas.columns[corr_gwas.columns.isin(intersection.values)]]
corr_gwas = corr_gwas.loc[intersection.values]
corr_gwas_sd = corr_gwas_sd[corr_gwas_sd.columns[corr_gwas_sd.columns.isin(intersection.values)]]
corr_gwas_sd = corr_gwas_sd.loc[intersection.values]
df_perf = df_perf.loc[intersection.values]
score_matrix =  np.tile(df_perf, (len(df_perf), 1))
df_heritability = df_heritability.loc[intersection.values]
score_heritability =  np.tile(df_heritability, (len(df_heritability), 1))
score_matrix_y = score_matrix.T
score_heritability_y = score_heritability.T


print(score_matrix.shape, score_heritability.shape, score_matrix_y.shape, score_heritability_y.shape, corr_gwas_sd.shape)
customdata = np.dstack((score_matrix, score_heritability, score_matrix_y, score_heritability_y, corr_gwas_sd))
hovertemplate = 'Model x: %{x}\
                 <br>Score x : %{customdata[0]:.3f}\
                 <br>Heritability x : %{customdata[1]:.3f}\
                 <br>\
                 <br>Model y : %{y}\
                 <br>Score y : %{customdata[2]:.3f}\
                 <br>Heritability y : %{customdata[3]:.3f}\
                 <br>\
                 <br>Correlation : %{z:.3f} ± %{customdata[4]:.3f}'
colorscale = get_colorscale(corr_gwas)
d = {}
d['data'] = [
    go.Heatmap(z=corr_gwas,
               x=corr_gwas.index,
               y=corr_gwas.columns,
               colorscale=colorscale,
               customdata=customdata,
               hovertemplate=hovertemplate,
               hoverongaps = False),
    ]
d['layout'] = {'width' : 1000, 'height' : 1000}

layout = dbc.Container([
                html.H1('GWAS - Correlations'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col(
                        [dcc.Graph(
                             id='Plot_GWAS_Corr',
                             figure = go.Figure(d)
                             ),
                         ],
                        style={ 'overflowX': 'scroll', 'width' : 800},
                         md=9)
                        ])
            ], fluid = True)
