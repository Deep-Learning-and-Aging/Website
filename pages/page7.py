import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS
import pandas as pd
import plotly.graph_objs as go
from .tools import get_colorscale

from app import app, MODE, filename
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
organs = ['Eyes','FullBody','Heart','Hips','Pancreas','Knees','Liver','Spine','Brain','Carotids']

path_scores_ewas = filename + 'page7_MultivariateXWASResults/Scores/'
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
dict_step_to_proper = dict(zip(['training', 'validation', 'test'], ['train', 'val', 'test']))
## Old just to test :
organs = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'HeartImages', 'LiverImages'])
if MODE != 'All':
    organs = [MODE]
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
            value = 'test'
            ),
        html.Br()
    ], id = 'Select_step_ewas_scores'),
    dbc.FormGroup([
        html.P("View Scores by : "),
        dcc.RadioItems(
            id = 'Select_view_type',
            options = get_dataset_options(['Organ', 'X']),
            value = 'Organ',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
        )
    ])

])


layout = dbc.Container([
                html.H1('Multivariate XWAS'),
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
             [Input('Select_algorithm', 'value'), Input('Select_step_scores_ewas', 'value'), Input('Select_data_type_scores', 'value'), Input('Select_view_type', 'value')])
def _compute_plots(algo, step, group, view_type):
    if algo is not None and step is not None:

        df = pd.read_csv(path_scores_ewas + 'Scores_%s_%s.csv' % (algo, dict_step_to_proper[step]))
        if group is not None and group != 'All':
            df  = df[df.subset == group]

        if MODE != 'All':
            df = df[df.organ == MODE]
        df_pivot = pd.pivot_table(df, values = 'r2', index = 'env_dataset', columns = 'organ')
        df_pivot_without_negative = df_pivot.clip(lower = 0)
        d = dict()
        print(get_colorscale(df_pivot_without_negative))

        hovertemplate = 'X dataset : %{y}\
                         <br>Organ : %{x}\
                         <br>R2 Score : %{customdata}'
        d['data'] = [
            go.Heatmap(z=df_pivot_without_negative,
                   x=df_pivot_without_negative.columns,
                   y=df_pivot_without_negative.index,
                    #hoverongaps = False,
                    colorscale=get_colorscale(df_pivot_without_negative),
                    customdata = df_pivot.round(4),
                    hovertemplate = hovertemplate,
                    )
            ]

        d2 = dict()
        if view_type == 'Organ':
            d2['data'] = [
                go.Bar(name = organ, x = df[df.organ == organ].env_dataset, y = df[df.organ == organ].r2, error_y = dict(type = 'data', array = df[df.organ == organ]['std'])) for organ in df.organ.drop_duplicates()
            ]
        elif view_type == 'X':
            d2['data'] = [
                go.Bar(name = x_dataset, x = df[df.env_dataset == x_dataset].organ, y = df[df.env_dataset == x_dataset].r2, error_y = dict(type = 'data', array = df[df.env_dataset == x_dataset]['std'])) for x_dataset in df.env_dataset.drop_duplicates()
            ]


        return go.Figure(d), go.Figure(d2)
    else :
        return go.Figure(), go.Figure()
