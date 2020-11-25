import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, empty_graph, load_csv
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import plotly.figure_factory as ff
from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64
from plotly.subplots import make_subplots
## Set performance file
performances = 'page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_eids_Age_test.csv'
## Set heritability file
filename_heritabilty = 'page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv'
## Set heritability file
filename_gwas_corr = 'page17_GWASCorrelations/'




def create_dfs(mode = MODE):
    df_perf = load_csv(performances).set_index('version')
    scores_organs = [elem.split('_')[1] for elem in df_perf.index.values]
    scores_view = [(elem.split('_')[2]).replace('*', '').replace('HearingTest', '').replace('BloodCount', '') for elem in df_perf.index.values]
    df_perf.index = [organ + view for organ, view in zip(scores_organs, scores_view)]
    df_perf = df_perf['R-Squared_all']

    df_heritability = load_csv(filename_heritabilty).set_index('Organ')['h2']
    corr_gwas = load_csv(filename_gwas_corr + 'GWAS_correlations_Age.csv').set_index('Unnamed: 0')
    corr_gwas_sd = load_csv(filename_gwas_corr + 'GWAS_correlations_sd_Age.csv').set_index('Unnamed: 0')

    if mode != 'All' :
        corr_gwas = corr_gwas[corr_gwas.columns[corr_gwas.columns.str.contains(mode)]]
        corr_gwas = corr_gwas.loc[corr_gwas.index.str.contains(mode)]
        corr_gwas_sd = corr_gwas_sd[corr_gwas_sd.columns[corr_gwas_sd.columns.str.contains(mode)]]
        corr_gwas_sd = corr_gwas_sd.loc[corr_gwas_sd.index.str.contains(mode)]

    ## Create intersection :
    intersection = df_perf.index.intersection(corr_gwas.index).intersection(df_heritability.index)
    corr_gwas = corr_gwas[corr_gwas.columns[corr_gwas.columns.isin(intersection.values)]]
    corr_gwas = corr_gwas.loc[intersection.values]
    corr_gwas_sd = corr_gwas_sd[corr_gwas_sd.columns[corr_gwas_sd.columns.isin(intersection.values)]]
    corr_gwas_sd = corr_gwas_sd.loc[intersection.values]

    ## Create matrixes :
    df_perf = df_perf.loc[intersection.values]
    df_heritability = df_heritability.loc[intersection.values]

    organ_sorted_by_score = df_perf.sort_values().index
    organ_sorted_alphabetically = df_perf.index.sort_values()
    return corr_gwas, corr_gwas_sd, df_perf, df_heritability, organ_sorted_by_score, organ_sorted_alphabetically


layout = dbc.Container([
                html.H1('Genetics - Correlations'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([
                        dbc.FormGroup([
                            html.P("Order by: "),
                            dcc.Dropdown(
                                id='Select_ordering_gwas_',
                                options = get_dataset_options(['Score', 'Custom', 'Clustering']),
                                value = 'Clustering'
                                ),
                            html.Br()
                        ])
                    ],md = 3),
                dbc.Col(
                    [dcc.Graph(
                         id='Plot_GWAS_Corr_'
                         ),
                     ],
                     md=9,
                     style={ 'overflowX': 'scroll', 'width' : 800},
                     )
                    ])
                ], fluid = True)


@app.callback(Output('Plot_GWAS_Corr_', 'figure'),
             [Input('Select_ordering_gwas_', 'value')])
def _plot_heatmap_(value_ordering):
    corr_gwas, corr_gwas_sd, df_perf, df_heritability, organ_sorted_by_score, organ_sorted_alphabetically = create_dfs(mode = MODE)
    if value_ordering is not None :
        if value_ordering == 'Score':
            ## Sort by score :
            df_perf = df_perf.loc[organ_sorted_by_score]
            df_heritability = df_heritability.loc[organ_sorted_by_score]

            corr_gwas = corr_gwas.loc[organ_sorted_by_score, organ_sorted_by_score]
            corr_gwas_sd = corr_gwas_sd.loc[organ_sorted_by_score, organ_sorted_by_score]

        elif value_ordering == 'Custom':
            ## Sort alphabetically
            df_perf = df_perf.loc[organ_sorted_alphabetically]
            df_heritability = df_heritability.loc[organ_sorted_alphabetically]

            corr_gwas = corr_gwas.loc[organ_sorted_alphabetically, organ_sorted_alphabetically]
            corr_gwas_sd = corr_gwas_sd.loc[organ_sorted_alphabetically, organ_sorted_alphabetically]

        elif value_ordering == 'Clustering':
            d2 = ff.create_dendrogram(corr_gwas.fillna(0), labels = corr_gwas.index)
            dendro_leaves = d2['layout']['xaxis']['ticktext']
            organ_sorted_cluster = dendro_leaves
            ## Sort alphabetically
            df_perf = df_perf.loc[organ_sorted_cluster]
            df_heritability = df_heritability.loc[organ_sorted_cluster]

            corr_gwas = corr_gwas.loc[organ_sorted_cluster, organ_sorted_cluster]
            corr_gwas_sd = corr_gwas_sd.loc[organ_sorted_cluster, organ_sorted_cluster]

        score_matrix =  np.tile(df_perf, (len(df_perf), 1))
        score_heritability =  np.tile(df_heritability, (len(df_heritability), 1))

        score_matrix_y = score_matrix.T
        score_heritability_y = score_heritability.T




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
        d['layout'] = {'width' : 800, 'height' : 800}

        if value_ordering == 'Clustering' :
            fig = make_subplots(rows=2, cols=1,
                                shared_xaxes=True,
                                vertical_spacing=0.02)
            for elem in d['data']:
                fig.add_trace(elem, row = 2, col = 1)
            for elem in d2['data']:
                elem['showlegend'] = False
                fig.add_trace(elem, row = 1, col = 1)

            fig['layout']['xaxis']['range'] = [0, 100]
            fig['layout']['xaxis']['showgrid'] = False
            fig['layout']['yaxis']['domain'] = [0.7, 1.0]
            fig['layout']['yaxis']['showticklabels'] = False
            fig['layout']['yaxis']['showgrid'] = False
            fig['layout']['yaxis2']['domain'] = [0, 0.7]
            fig['layout']['yaxis2']['showgrid'] = False
            fig['layout']['width'] = 900
            fig['layout']['height'] = 900
            fig['layout']['xaxis']['autorange'] =  True
            return fig
        else :
            return go.Figure(d)
    else :
        return go.Figure(empty_graph)
