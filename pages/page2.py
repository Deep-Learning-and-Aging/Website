import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
import numpy as np

distinct_colors = ['#e6194b', '#3cb44b', '#ffe119', '#4363d8', '#f58231', '#911eb4', '#46f0f0', '#f032e6', '#bcf60c', '#fabebe', '#008080', '#e6beff', '#9a6324', '#fffac8', '#800000', '#aaffc3', '#808000', '#ffd8b1', '#000075', '#808080', '#ffffff', '#000000']

path_performance = '/Users/samuel/Desktop/dash_app/for_Samuel/'
organs = ['Eyes','FullBody','Heart','Hips','Pancreas','Knees','Liver','Spine','Brain','Carotids']

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select eid vs instances : "),
        dcc.RadioItems(
            id = 'select_eid_or_instances',
            options = get_dataset_options(['eids', 'instances']),
            value = 'instances',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select aggregate type : "),
        dcc.RadioItems(
            id ='select_aggregate_type',
            options = get_dataset_options(['bestmodels', 'withEnsembles', 'tuned']),
            value = 'bestmodels',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ',
            options = get_dataset_options(organs + ['All']),
            placeholder = 'All',
            value = 'All'
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select step : "),
        dcc.Dropdown(
            id='Select_step',
            options = get_dataset_options(['Train', 'Test', 'Validation']),
            value = 'Test'
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select a scoring metric : "),
        dcc.RadioItems(
            id='Select_metric',
            options = get_dataset_options(['RMSE', 'R2']),
            value = 'R2',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ])
])


layout = dbc.Container([
                html.H1('Age Prediction Scores'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [dcc.Graph(
                             id='Plot R2 scores'
                             ),
                         ],
                        style={'overflowY': 'scroll', 'height': 600, 'overflowX': 'scroll', 'width' : 700},
                         md=9)
                        ])
            ], fluid = True)

# @app.callback(Output('Plot R2 scores', 'figure'),
#               [Input('select_eid_or_instances', 'value'), Input('select_aggregate_type', 'value'), Input('Select_organ', 'value')])
# def _plot_r2_scores(value_eid_vs_instances, value_aggregate, value_organ):
#
#     df = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_test.csv' % (value_aggregate, value_eid_vs_instances))
#     df_res = df[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
#     df_res = df_res.sort_values(['organ', 'view', 'transformation', 'architecture'])
#
#     df_val = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_val.csv' % (value_aggregate, value_eid_vs_instances))
#     df_res_val = df_val[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
#     df_res_val = df_res_val.sort_values(['organ', 'view', 'transformation', 'architecture'])
#
#     df_train = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_train.csv' % (value_aggregate, value_eid_vs_instances))
#     df_res_train = df_train[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
#     df_res_train = df_res_train.sort_values(['organ', 'view', 'transformation', 'architecture'])
#
#     print(df_res)
#     if value_organ != 'All':
#
#
#         df_res = df_res[df_res.organ == value_organ]
#         df_res_val = df_res_val[df_res_val.organ == value_organ]
#         df_res_train = df_res_train[df_res_train.organ == value_organ]
#         y = df_res['R-Squared_all']
#         y_train = df_res_train['R-Squared_all']
#         y_val = df_res_val['R-Squared_all']
#
#         if value_organ in ['Heart', 'Liver', 'Pancreas']:
#
#             x = [df_res['view'].values, df_res['transformation'].values]
#             distinct_architectures = df_res.architecture.drop_duplicates()
#             n_archi = len(distinct_architectures)
#             opacity_range = np.linspace(0, 50, n_archi)
#             map_archi_opacity = dict(zip(list(distinct_architectures), opacity_range))
#
#             list_plot = []
#
#             for idx, archi in enumerate(distinct_architectures):
#                 color = distinct_colors[idx]
#                 plot_test = go.Bar(x = [df_res[df_res.architecture == archi]['view'].values, df_res[df_res.architecture == archi]['transformation'].values],
#                                    y = df_res[df_res.architecture == archi]['R-Squared_all'],
#                                    marker=dict(color = color,
#                                                line = dict(width = 3, color = 'Black')),
#                                    name=archi,
#                                    legendgroup=archi,
#                                    showlegend=False
#                                   )
#                 plot_val = go.Bar(x = [df_res[df_res.architecture == archi]['view'].values, df_res[df_res.architecture == archi]['transformation'].values],
#                                   y = df_res_val[df_res_val.architecture == archi]['R-Squared_all'],
#                                   legendgroup = archi,
#                                   name=archi,
#                                   marker=dict(color = color,
#                                               line = dict(width = 1.5, color = 'Black')),
#                                   showlegend=False
#                                   )
#                 plot_train = go.Bar(x = [df_res[df_res.architecture == archi]['view'].values, df_res[df_res.architecture == archi]['transformation'].values],
#                                     y = df_res_train[df_res_train.architecture == archi]['R-Squared_all'],
#                                     legendgroup = archi,
#                                     name=archi,
#                                     marker=dict(color = color,
#                                                 line = dict(width = 0, color = 'Black')),
#                                     showlegend=True
#                                     )
#                 list_plot.append(plot_test)
#                 list_plot.append(plot_val)
#                 list_plot.append(plot_train)
#
#             d = {'data' : list_plot,
#                  'layout' : dict(height = 1000,
#                                  margin={'l': 40, 'b': 30, 't': 10, 'r': 0})}
#             print(d)
#
#         elif value_organ in ['Carotids', 'Eyes', 'FullBody', 'Hips', 'Knees', 'Spine', 'Brain']:
#             x = [df_res['view'].values, df_res['architecture'].values]
#             d = {'data' : [go.Bar(x = x, y = y, name = 'test', showlegend = False, marker = dict(color='Green')),
#                        go.Bar(x = x, y = y_train, name = 'train', showlegend = False, marker = dict(color='Orange')),
#                        go.Bar(x = x, y = y_val, name = 'val', showlegend = False, marker = dict(color='Red'))],
#                        'layout' : dict(height = 1000,
#                              margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
#                              barmode='group')}
#
#         return go.Figure(d)
#     else :
#         return go.Figure()


@app.callback(Output('Plot R2 scores', 'figure'),
              [Input('select_eid_or_instances', 'value'), Input('select_aggregate_type', 'value'), Input('Select_organ', 'value'), Input('Select_step', 'value'), Input('Select_metric', 'value')])
def _plot_r2_scores(value_eid_vs_instances, value_aggregate, value_organ, value_step, value_metric):
    if value_metric == 'R2':
        metric = 'R-Squared_all'
        std = 'R-Squared_sd_all'
    elif value_metric == 'RMSE':
        metric = 'RMSE_all'
        std = 'RMSE_sd_all'

    else :
        raise ValueError("WRONG METRIC ! ")
    if value_step == 'Validation':
        df = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_val.csv' % (value_aggregate, value_eid_vs_instances))
        df_res = df[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
        df_res = df_res.sort_values(['organ', 'view', 'transformation', 'architecture'])

    elif value_step == 'Train':
        df = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_train.csv' % (value_aggregate, value_eid_vs_instances))
        df_res = df[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
        df_res = df_res.sort_values(['organ', 'view', 'transformation', 'architecture'])

    elif value_step == 'Test':
        df = pd.read_csv(path_performance + 'PERFORMANCES_%s_ranked_%s_Age_test.csv' % (value_aggregate, value_eid_vs_instances))
        df_res = df[['target', 'organ', 'view', 'transformation', 'architecture', 'RMSE_all', 'RMSE_sd_all', 'R-Squared_all', 'R-Squared_sd_all']]
        df_res = df_res.sort_values(['organ', 'view', 'transformation', 'architecture'])

    if value_organ == 'All':
        distinct_architectures = df_res.architecture.drop_duplicates()
        plots = []

        for archi in distinct_architectures:
            df_res_archi = df_res[df_res.architecture == archi]
            df_res_archi['view'] = df_res_archi['view'] + ' - ' + df_res_archi['transformation']
            df_res_archi['view'] = df_res_archi['view'].str.replace('- raw', '')
            plot_test = go.Bar(x = [df_res_archi[df_res_archi.architecture == archi]['organ'].values,
                                    df_res_archi[df_res_archi.architecture == archi]['view'].values],
                               y = df_res_archi[df_res_archi.architecture == archi][metric],
                               error_y=dict(type='data', array=df_res_archi[df_res_archi.architecture == archi][std]),
                               name = archi)
            plots.append(plot_test)

        d = {'data' : plots,
             'layout' : dict(height = 600,
                             width = max(20*len(df_res['architecture']), 850),
                             margin = {'l': 40, 'b': 0, 't': 10, 'r': 40},
                             legend= dict(orientation='h',
                                          x = 0,
                                          y = -0.4))}

    elif value_organ in ['Heart', 'Liver', 'Pancreas']:
        df_res = df_res[df_res.organ == value_organ]
        distinct_architectures = df_res.architecture.drop_duplicates()
        plots = []
        for archi in distinct_architectures:
            plot_test = go.Bar(x = [df_res[df_res.architecture == archi]['view'].values,
                                    df_res[df_res.architecture == archi]['transformation'].values],
                               y = df_res[df_res.architecture == archi][metric],
                               error_y = dict(type='data', array=df_res[df_res.architecture == archi][std]),
                               name = archi)
            plots.append(plot_test)
        d = {'data' : plots,
             'layout' : dict(height = 600,
                             width = max(25*len(df_res['architecture']), 850),
                             margin = {'l': 40, 'b': 0, 't': 10, 'r': 40},
                             legend=dict(orientation='h',
                                         y = -0.4))}
    elif value_organ in  ['Carotids', 'Eyes', 'FullBody', 'Hips', 'Knees', 'Spine', 'Brain']:
        df_res = df_res[df_res.organ == value_organ]
        distinct_architectures = df_res.architecture.drop_duplicates()
        plots = []
        for archi in distinct_architectures:
            plot_test = go.Bar(x = df_res[df_res.architecture == archi]['view'].values,
                               y = df_res[df_res.architecture == archi][metric],
                               error_y = dict(type='data', array=df_res[df_res.architecture == archi][std]),
                               name = archi)
            plots.append(plot_test)
        d = {'data' : plots,
             'layout' : dict(height = 600,
                             width = max(25*len(df_res['architecture']), 850),
                             margin = {'l': 40, 'b': 0, 't': 10, 'r': 40},
                             legend=dict(orientation='h',
                                         y = -0.4))}


    return go.Figure(d)
