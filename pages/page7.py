import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS
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

path_linear_ewas = '/Users/samuel/Desktop/dash_app/data/linear_output_v2/'
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
              'BoneDensitometryOfHeel', 'HearingTest', 'AnthropometryAllBiomarkers'])
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = sorted(Environmental + Biomarkers + Pathologies)

## Old just to test :
organs = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'HeartImages', 'LiverImages'])

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select data type: "),
        dcc.RadioItems(
            id='Select_data_type_scores',
            options = get_dataset_options(['All', 'Biomarkers', 'Pathologies', 'Environmental']),
            value = 'All',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select an Algorithm : "),
        dcc.Dropdown(
            id='Select_algorithm',
            options = get_dataset_options(['ElasticNet', 'LightGbm', 'NeuralNetwork', 'BestOfThem']),
            value = 'LightGbm'
            ),
        html.Br()
    ], id = 'Select_dataset_ewas_full'),
    dbc.FormGroup([
        html.P("Select step  : "),
        dcc.Dropdown(
            id='Select_step_scores_ewas',
            options = get_dataset_options(['training', 'validation', 'test']),
            placeholder = 'test',
            value = 'HeartImages'
            ),
        html.Br()
    ], id = 'Select_step_ewas_scores'),

])


layout = dbc.Container([
                html.H1('Scores Multivariate XWAS'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [dcc.Loading([
                            dcc.Graph(
                             id='Plot R2 Heatmap'
                             )]
                            )],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ]),
                dbc.Row([
                    dbc.Col([
                            dcc.Graph(
                                id = 'Plot Bar Plot'
                            )
                         ],
                            style={'overflowX': 'scroll', 'width' : 1000})
                    ])
            ], fluid = True)



@app.callback([Output('Plot R2 Heatmap', 'figure'), Output('Plot Bar Plot', 'figure')],
             [Input('Select_algorithm', 'value'), Input('Select_step_scores_ewas', 'value'), Input('Select_data_type_scores', 'value')])
def _compute_plots(algo, step, group):
    return go.Figure(), go.Figure()
