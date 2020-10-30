import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, empty_graph
import pandas as pd
import plotly.graph_objs as go

from app import app
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
organs = ['Eyes','FullBody','Heart','Hips','Pancreas','Knees','Liver','Spine','Brain','Carotids']

path_correlations_ewas = './' + app.get_asset_url('page8_MultivariateXWASCorrelations/CorrelationsMultivariate/')
Environmental = sorted(['Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivity', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors'])
Biomarkers = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest'])
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = sorted(Environmental + Biomarkers + Pathologies)
organs = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'HeartImages', 'LiverImages'])

colorscale =  [[0, 'rgba(255, 0, 0, 0.85)'],
               [0.5, 'rgba(255, 255, 255, 0.85)'],
               [1, 'rgba(0, 0, 255, 0.85)']]
#
# controls = dbc.Row([
#     dbc.Col([
#         dbc.Card([
#             dbc.Row([
#                 dbc.Col([
#                     dbc.FormGroup([
#                         dbc.Label("Select correlation type :"),
#                         dcc.RadioItems(
#                             id='Select_corr_type_mul_ewas',
#                             options = get_dataset_options(['Pearson', 'Spearman']),
#                             value = 'Pearson',
#                             labelStyle = {'display': 'inline-block', 'margin': '5px'}
#                             )
#                     ])
#                 ], width={"size": 6}),
#                 dbc.Col([
#                     dbc.Label("Select Algorithm :"),
#                     dcc.Dropdown(
#                         id='Select_algorithm_method',
#                         options = get_dataset_options(['LightGbm', 'NeuralNetwork', 'ElasticNet']),
#                         placeholder = 'LightGbm',
#                         value = 'LightGbm',
#                         )
#                 ], width={"size": 6})
#             ])
#         ])
# #], width={"size": 8, "offset": 2})
# ], width={"size": 8})
# ])
#
#
#
# layout =  dbc.Container([
#                 html.H1('Multivariate XWAS - Correlation'),
#                 html.Br(),
#                 html.Br(),
#                 dcc.Loading([
#                     dcc.Store(id='memory_corr_ewas_mul'),
#                     dbc.Row([
#                         dbc.Col([controls])
#                         ]),
#                     html.Br(),
#                     html.Hr(),
#                     dbc.Row([
#                         dbc.Col([
#                             dbc.Card([
#                                 dbc.FormGroup([
#                                     html.P("Select Environmental Dataset: "),
#                                     dcc.Dropdown(
#                                         id='Select_env_dataset_mul_ewas',
#                                         options = get_dataset_options(sorted(All)),
#                                         value = sorted(All)[0]
#                                         ),
#                                     html.Br()
#                                     ], id = 'Select_env_dataset_mul_ewas_full')
#                                 ])
#                             ]),
#                         dbc.Col([
#                             dcc.Graph(id='Correlation Mul - Select Ewas dataset')
#                             ], md=9)
#                         ]),
#                     html.Br(),
#                     html.Hr(),
#                     dbc.Row([
#                         dbc.Col([
#                             dbc.Card([
#                                 dbc.FormGroup([
#                                     html.P("Select an Organ : "),
#                                     dcc.Dropdown(
#                                         id='Select_organ_mul_ewas',
#                                         options = get_dataset_options(organs),
#                                         value = sorted(organs)[0],
#                                         ),
#                                     html.Br()
#                                     ], id = 'Select_organ_mul_ewas_full')
#                                 ])
#                             ]),
#                         dbc.Col([
#                             dcc.Graph(id='Correlation Mul - Select Organ')
#                             ], md=9)
#                         ])
#                     ])
#                 ],
#                 fluid = True)
#
#
# @app.callback(Output('memory_corr_ewas_mul', 'data'),
#              [Input('Select_corr_type_mul_ewas', 'value'), Input('Select_algorithm_method', 'value')])
# def _load_data_in_mem(value_corr_type, value_subset):
#     if value_corr_type is not None and value_subset is not None:
#         df = pd.read_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (value_corr_type, value_subset))
#         df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
#         return df.to_dict('records')
#
#
# @app.callback(Output('Correlation Mul - Select Ewas dataset', 'figure'),
#              [Input('memory_corr_ewas_mul', 'data'), Input('Select_env_dataset_mul_ewas', 'value')])
# def _plot_with_given_env_dataset(data, env_dataset):
#     df = pd.DataFrame(data = data)
#     df_env = df[df.env_dataset == env_dataset]
#     matrix_env = pd.pivot_table(df_env, values='corr', index=['organ_1'],
#                     columns=['organ_2'])
#
#     d = {}
#     d['data'] = go.Heatmap(z=matrix_env,
#                x=matrix_env.index,
#                y=matrix_env.columns,
#                colorscale = colorscale)
#     d['layout'] = dict(xaxis = dict(dtick = 1),
#                        yaxis = dict(dtick = 1),
#                        width = 600,
#                        height = 600)
#
#     return go.Figure(d)
#
# @app.callback(Output('Correlation Mul - Select Organ', 'figure'),
#              [Input('memory_corr_ewas_mul', 'data'), Input('Select_organ_mul_ewas', 'value')])
# def _plot_with_given_organ_dataset(data, organ):
#     df = pd.DataFrame(data = data)
#     df_organ = df[df.organ_1 == organ]
#     df_organ = df_organ[df_organ.organ_2 != organ]
#     matrix_organ = pd.pivot_table(df_organ, values='corr', index=['env_dataset'],
#                     columns=['organ_2'])
#     print(matrix_organ)
#     print(matrix_organ.index)
#     d = {}
#     d['data'] = go.Heatmap(z=matrix_organ.T,
#                x=matrix_organ.T.columns,
#                y=matrix_organ.T.index,
#                colorscale = colorscale)
#     d['layout'] = dict(xaxis = dict(dtick = 1),
#                        yaxis = dict(dtick = 1),
#                        width = 1000,
#                        height = 600)
#     return go.Figure(d)




controls1 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_mul_ewas1',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_algorithm_method1',
            options = get_dataset_options(['LightGbm', 'ElasticNet', 'NeuralNetwork']),
            placeholder = 'LightGbm',
            value = 'LightGbm',
            )
    ]),
    dbc.FormGroup([
        html.P("Select an X Dataset: "),
        dcc.Dropdown(
            id='Select_env_dataset_mul_ewas',
            options = get_dataset_options(sorted(All)),
            value = sorted(All)[0]
            ),
        html.Br()
        ])
])

controls2 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_mul_ewas2',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_algorithm_method2',
            options = get_dataset_options(['LightGbm', 'ElasticNet', 'NeuralNetwork']),
            placeholder = 'LightGbm',
            value = 'LightGbm',
            )
    ]),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_mul_ewas',
            options = get_dataset_options(organs),
            value = sorted(organs)[0],
            ),
        html.Br()
        ])
])

layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label = 'Select X', tab_id='tab_X'),
        dbc.Tab(label = 'Select Organ', tab_id = 'tab_organ'),
    ], id = 'tab_manager_mul', active_tab = 'tab_X'),
    html.Div(id="tab-content_mul")
])


@app.callback(Output('tab-content_mul', 'children'),
             [Input('tab_manager_mul', 'active_tab')])
def _plot_with_given_env_dataset(ac_tab):
    if ac_tab == 'tab_X':
        return  dbc.Container([
                        html.H1('Multivariate XWAS - Correlations between accelerated aging'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls1,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    dcc.Graph(id='Correlation Mul - Select Ewas dataset')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)
    elif ac_tab == 'tab_organ':
        return  dbc.Container([
                        html.H1('Multivariate XWAS - Correlations between accelerated aging'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls2,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    dcc.Graph(id='Correlation Mul - Select Organ')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)


@app.callback(Output('Correlation Mul - Select Ewas dataset', 'figure'),
             [Input('Select_corr_type_mul_ewas1', 'value'), Input('Select_algorithm_method1', 'value'), Input('Select_env_dataset_mul_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, env_dataset):
    if corr_type is not None and subset_method is not None:
        df = pd.read_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, subset_method))
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
        df_env = df[df.env_dataset == env_dataset]
        matrix_env = pd.pivot_table(df_env, values='corr', index=['organ_1'],
                        columns=['organ_2'])
        colorscale =  get_colorscale(matrix_env)
        d = {}
        d['data'] = go.Heatmap(z=matrix_env,
                   x=matrix_env.index,
                   y=matrix_env.columns,
                   colorscale = colorscale)
        d['layout'] = dict(xaxis = dict(dtick = 1),
                           yaxis = dict(dtick = 1),
                           width = 800,
                           height = 800)
        return go.Figure(d)
    else:
        return go.Figure()


@app.callback(Output('Correlation Mul - Select Organ', 'figure'),
             [Input('Select_corr_type_mul_ewas2', 'value'), Input('Select_algorithm_method2', 'value'), Input('Select_organ_mul_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, organ):
    if corr_type is not None and subset_method is not None:
        df = pd.read_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, subset_method))
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
        df_organ = df[df.organ_1 == organ]
        df_organ = df_organ[df_organ.organ_2 != organ]
        matrix_organ = pd.pivot_table(df_organ, values='corr', index=['env_dataset'],
                        columns=['organ_2'])
        print(matrix_organ)
        colorscale =  get_colorscale(matrix_organ)
        d = {}
        d['data'] = go.Heatmap(z=matrix_organ.T,
                   x=matrix_organ.T.columns,
                   y=matrix_organ.T.index,
                   colorscale = colorscale)
        d['layout'] = dict(xaxis = dict(dtick = 1),
                           yaxis = dict(dtick = 1),
                           width = 1000,
                           height = 600)
        return go.Figure(d)
    else :
        return go.Figure()
