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

filename_volcano = filename + 'page10_GWASResults/Volcano/GWAS_hits_Age_'
filename_manhattan = filename + 'page10_GWASResults/Manhattan/GWAS_ManhattanPlot_Age_'

list_files_volcano = glob.glob(filename_volcano + '*')
list_files_volcano = [elem.split('/')[-1] for elem in list_files_volcano]
organs_gwas_volcano = sorted([elem.split('_')[3].replace('.csv', '') for elem in list_files_volcano])#['Heart']

list_files_manhattan = glob.glob(filename_manhattan + '*')
list_files_manhattan = [elem.split('/')[-1] for elem in list_files_manhattan]
organs_gwas_manhattan = sorted([elem.split('_')[3].replace('.png', '') for elem in list_files_manhattan])#['Heart']

dict_chr_to_colors = {'1': '#b9b8b5', '2': '#222222', '3': '#f3c300', '4': '#875692', '5': '#f38400', '6': '#a1caf1',
                      '7': '#be0032', '8': '#c2b280', '9': '#848482', '10': '#008856', '11': '#555555',
                      '12': '#0067a5', '13': '#f99379', '14': '#604e97', '15': '#f6a600', '16': '#b3446c',
                      '17': '#dcd300', '18': '#882d17', '19': '#8db600', '20': '#654522', '21': '#e25822',
                      '22': '#232f00', '23': '#e68fac'}

#layout = html.Div([], id = 'id_menu')
if MODE != 'All' :
    #style = {'display' : 'None'}
    organs_gwas_volcano = [elem for elem in organs_gwas_volcano if MODE in elem ]
    organs_gwas_manhattan = [elem for elem in organs_gwas_manhattan if MODE in elem ]
    value_volcano = organs_gwas_volcano[0]
    value_manhattan = organs_gwas_manhattan[0]
else :
    #style = {}
    value_volcano = 'All'
    value_manhattan = 'All'

controls1 = dbc.Card([
    dbc.FormGroup([
        html.P("Select an organ: "),
        dcc.Dropdown(
            id='select_organ',
            options = get_dataset_options(organs_gwas_manhattan),
            value = value_manhattan
            ),
        html.Br()
    ])
])

controls2 = dbc.Card([
    dbc.FormGroup([
        html.P("Select an organ: "),
        dcc.Dropdown(
            id='select_organ2',
            options = get_dataset_options(organs_gwas_volcano),
            value = value_volcano
            ),
        html.Br()
    ])
])




layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label = 'Manhattan Plot', tab_id='man_plot'),
        dbc.Tab(label = 'Volcano Plot', tab_id = 'vol_plot'),
    ], id = 'tab_manager_gwas', active_tab = 'vol_plot'),
    html.Div(id="tab_content_gwas")
])

@app.callback(Output('tab_content_gwas', 'children'),
             [Input('tab_manager_gwas', 'active_tab')])
def _plot_with_given_env_dataset(ac_tab):
    if ac_tab == 'man_plot':
        return  dbc.Container([
                        html.H1('GWAS - Manhattan Plot '),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls1,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    html.Img(id = 'mana_plot', style={'height':'50%', 'width':'50%'})
                                    #dcc.Graph(id = 'mana_plot')
                                 ])],
                                md=9)
                                ])
                        ], fluid = True)
    elif ac_tab == 'vol_plot':
        return  dbc.Container([
                        html.H1('GWAS - Volcano Plot'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls2,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    dcc.Graph(id='vol_plot')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)


@app.callback(Output('mana_plot', 'src'),
             [Input('select_organ', 'value')])
def _plot_manhattan_plot(organ):
    if organ is not None:
        path_png = filename_manhattan + organ + '.png'
        img_base64 = base64.b64encode(open(path_png, 'rb').read()).decode('ascii')
        src='data:image/png;base64,{}'.format(img_base64)
        return src
    else :
        return ''


@app.callback(Output('vol_plot', 'figure'),
             [Input('select_organ2', 'value')])
def _plot_volcano_plot(organ):
    if organ is not None:
        d = {}
        if organ != 'All':
            df = pd.read_csv(filename_volcano + organ + '.csv')[['CHR', 'Gene', 'Gene_type', 'SNP', 'P_BOLT_LMM_INF', 'BETA']].sort_values('CHR')
            d['data'] = [go.Scatter(x = df[df.CHR == chromo]['BETA'],
                                    y = - np.log(df[df.CHR == chromo]['P_BOLT_LMM_INF']),
                                    mode = 'markers',
                                    name = 'CHR %s' % chromo,
                                    marker = dict(color =  dict_chr_to_colors[ str(chromo) ]),
                                    customdata = np.stack((df[df.CHR == chromo]['SNP'], df[df.CHR == chromo]['Gene'], df[df.CHR == chromo]['Gene_type']), axis = 1),
                                    hovertemplate = """SNP : %{customdata[0]}
                                                       <br> Gene : %{customdata[1]}
                                                       <br> Gene Type : %{customdata[2]}"""
                                    )  for chromo in df['CHR'].drop_duplicates()
                         ]
        else :
            df = pd.read_csv(filename_volcano + organ + '.csv')[['CHR', 'Gene', 'Gene_type', 'SNP', 'P_BOLT_LMM_INF', 'BETA', 'organ']].sort_values('CHR')
            d['data'] = [go.Scatter(x = df[df.CHR == chromo]['BETA'],
                                    y = - np.log(df[df.CHR == chromo]['P_BOLT_LMM_INF']),
                                    mode = 'markers',
                                    name = 'CHR %s' % chromo,
                                    marker = dict(color =  dict_chr_to_colors[ str(chromo) ]),
                                    customdata = np.stack((df[df.CHR == chromo]['SNP'], df[df.CHR == chromo]['organ'], df[df.CHR == chromo]['Gene'], df[df.CHR == chromo]['Gene_type']), axis = 1),
                                    hovertemplate = """SNP : %{customdata[0]}
                                                       <br> Organ : %{customdata[1]}
                                                       <br> Gene : %{customdata[2]}
                                                       <br> Gene Type : %{customdata[3]}"""
                                    )  for chromo in df['CHR'].drop_duplicates()
                         ]

        d['layout'] = dict(title={'text' : 'Volcano plot', 'x':0.5,},# title of plot
                           xaxis={'title' :'Size Effect (SE)'}, # xaxis label
                           yaxis={'title' :'-log(p_value)'}
                                )
        return go.Figure(d)
    else :
        return go.Figure()
