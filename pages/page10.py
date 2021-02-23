import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, load_csv, heritability, list_obj, encode_img_s3
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

performances = 'page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_eids_Age_test.csv'
df_perf = load_csv(performances).set_index('version')
scores_organs = [elem.split('_')[1] for elem in df_perf.index.values]
scores_view = [(elem.split('_')[2]).replace('*', '').replace('HearingTest', '').replace('BloodCount', '') for elem in df_perf.index.values]
df_perf.index = [organ + view for organ, view in zip(scores_organs, scores_view)]
df_perf = df_perf[['R-Squared_all', 'N_all']]


## Set heritability file
df_heritability = heritability.set_index('Organ')



filename_volcano = 'page10_GWASResults/Volcano/GWAS_hits_Age_'
filename_manhattan = 'page10_GWASResults/Manhattan/GWAS_ManhattanPlot_Age_'
filename_qq = 'page10_GWASResults/Manhattan/GWAS_QQPlot_Age_'
list_files_volcano = list_obj(filename_volcano)
list_files_volcano = [elem.split('/')[-1] for elem in list_files_volcano]
organs_gwas_volcano = sorted(list(set([elem.split('_')[3].replace('.csv', '') for elem in list_files_volcano])))#['Heart']

list_files_manhattan = list_obj(filename_manhattan)
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
    html.H1('Genetics - GWAS '),
    dbc.Tabs([
        dbc.Tab(label = 'Manhattan Plot', tab_id='man_plot'),
        dbc.Tab(label = 'Volcano Plot', tab_id = 'vol_plot'),
    ], id = 'tab_manager_gwas', active_tab = 'man_plot'),
    html.Div(id="tab_content_gwas")
])

@app.callback(Output('tab_content_gwas', 'children'),
             [Input('tab_manager_gwas', 'active_tab')])
def _plot_with_given_env_dataset(ac_tab):
    if ac_tab == 'man_plot':
        return  dbc.Container([
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls1,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [
                                dcc.Loading([
                                    html.H3(id = 'title_man'),
                                    html.H3('Manhattan Plot'),
                                    html.Img(id = 'mana_plot', style={'height':'70%', 'width':'70%'}),
                                    html.H3('QQ Plot'),
                                    html.Img(id = 'qq_plot', style={'height':'70%', 'width':'70%'})
                                    #dcc.Graph(id = 'mana_plot')
                                    ])
                                ],
                                md=9)
                                ])
                        ], fluid = True)
    elif ac_tab == 'vol_plot':
        return  dbc.Container([
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


@app.callback([Output('mana_plot', 'src'),Output('qq_plot', 'src'), Output('title_man', 'children')],
             [Input('select_organ', 'value')])
def _plot_manhattan_plot(organ):
    if organ is not None:
        path_man = filename_manhattan + organ + '.png'
        path_qq = filename_qq + organ + '.png'
        #buffered_man = BytesIO()
        #img_man.save(buffered_man, format="PNG")
        #buffered_qq = BytesIO()
        #img_qq.save(buffered_qq, format="PNG")

        #img_man64 = base64.b64encode(buffered_man.getvalue()).decode('ascii')
        #img_qq64 = base64.b64encode(buffered_qq.getvalue()).decode('ascii')

        img_man64=encode_img_s3(path_man)
        img_qq64=encode_img_s3(path_qq)
        src_man ='data:image/png;base64,{}'.format(img_man64)
        src_qq ='data:image/png;base64,{}'.format(img_qq64)
        if organ != 'All' :
            score = df_perf.loc[organ]['R-Squared_all']
            sample_size = int(df_perf.loc[organ]['N_all'])
            heritability = df_heritability.loc[organ]['h2']
            title = 'R-squared : %.3f, Sample Size : %d, Heritability : %.3f' % (score, sample_size, heritability)
        else :
            title = ''
        return src_man, src_qq, title
    else :
        return '', '', ''


@app.callback(Output('vol_plot', 'figure'),
             [Input('select_organ2', 'value')])
def _plot_volcano_plot(organ):
    if organ is not None:
        d = {}

        if organ != 'All':
            df = load_csv(filename_volcano + organ + '_withGenes.csv')[['CHR', 'Gene', 'Gene_type', 'SNP', 'P_BOLT_LMM_INF', 'BETA']].sort_values('CHR')
            d['data'] = [
                go.Scatter(x = [df['BETA'].min() - df['BETA'].std(), df['BETA'].max() + df['BETA'].std()],
                           y = [-np.log(5e-8), -np.log(5e-8)],
                           name = '*Significance level after FDR',
                           mode = 'lines')]
            d['data'] += [go.Scatter(x = df[df.CHR == chromo]['BETA'],
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
            df = load_csv(filename_volcano + organ + '_withGenes.csv')[['CHR', 'Gene', 'Gene_type', 'SNP', 'P_BOLT_LMM_INF', 'BETA', 'organ']].sort_values('CHR')
            d['data'] = [
                go.Scatter(x = [df['BETA'].min() - df['BETA'].std(), df['BETA'].max() + df['BETA'].std()],
                           y = [-np.log(5e-8), -np.log(5e-8)],
                           name = '*Significance level after FDR',
                           mode = 'lines')]
            d['data'] += [go.Scatter(x = df[df.CHR == chromo]['BETA'],
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
                           yaxis={'title' :'-log(p_value)'},
                           legend={'orientation' : 'h'},
                           margin = {'l': 0, 'b': 150, 't': 0, 'r': 0},
                           height = 700
                                )
        return go.Figure(d)
    else :
        return go.Figure()
