import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, heritability, load_csv
from pandas import pivot_table, concat
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
from .tools import get_colorscale, empty_graph

from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
step = 'test'
df_heritability = heritability.rename(columns = {'h2' : 'r2', 'h2_sd' : 'std', 'Organ' : 'organ'})
df_heritability['env_dataset'] = 'Genetics'
df_heritability['subset'] = 'Genetics'


path_scores_ewas = 'page7_MultivariateXWASResults/Scores/'
Environmental = sorted(['Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivity', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors', 'Smoking'])
Biomarkers = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemistry', 'BloodBiochemistry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraocularPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'AnthropometryAllBiomarkers', 'CognitiveFluidIntelligence',
              'CognitiveMatrixPatternCompletion', 'CognitiveNumericMemory', 'CognitivePairedAssociativeLearning',
              'CognitivePairsMatching', 'CognitiveProspectiveMemory', 'CognitiveReactionTime',
              'CognitiveSymbolDigitSubstitution', 'CognitiveTowerRearranging', 'CognitiveTrailMaking'])
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = sorted(Environmental + Biomarkers + Pathologies)
dict_step_to_proper = dict(zip(['training', 'validation', 'test'], ['train', 'val', 'test']))
## Old just to test :
organs = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])
if MODE != 'All':
    organs = [MODE]
controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select data type: "),
        dcc.RadioItems(
            id='Select_data_type_scores',
            options = get_dataset_options(['All', 'Biomarkers', 'Pathologies', 'Environmental', 'Genetics']),
            value = 'All',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select an Algorithm : "),
        dcc.Dropdown(
            id='Select_algorithm',
            options = get_dataset_options(['ElasticNet', 'LightGbm', 'NeuralNetwork', 'Best Algorithm']),
            value = 'Best Algorithm'
            ),
        html.Br()
    ], id = 'Select_dataset_ewas_full'),
    # dbc.FormGroup([
    #     html.P("Select step  : "),
    #     dcc.Dropdown(
    #         id='Select_step_scores_ewas',
    #         options = get_dataset_options(['training', 'validation', 'test']),
    #         value = 'test'
    #         ),
    #     html.Br()
    # ], id = 'Select_step_ewas_scores'),
    dbc.FormGroup([
        html.P("View R2 by : "),
        dcc.RadioItems(
            id = 'Select_view_type',
            options = get_dataset_options(['Organ', 'X']),
            value = 'Organ',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
        )
    ])

])


layout = dbc.Container([
                html.H1('Multivariate XWAS - Results'),
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
             [Input('Select_algorithm', 'value'),
              #Input('Select_step_scores_ewas', 'value'),
              Input('Select_data_type_scores', 'value'),
              Input('Select_view_type', 'value')])
def _compute_plots(algo, group, view_type):
    if algo is not None and step is not None:
        if algo != 'Best Algorithm' :
            df = load_csv(path_scores_ewas + 'Scores_%s_%s.csv' % (algo, dict_step_to_proper[step]), usecols = ['env_dataset', 'r2', 'std', 'organ', 'subset', 'sample_size'])
            df = concat([df, df_heritability])
        else :
            list_df = []
            for algo_ in ['LightGbm', 'NeuralNetwork', 'ElasticNet'] :
                df_algo = load_csv(path_scores_ewas + 'Scores_%s_%s.csv' % (algo_, dict_step_to_proper[step]), usecols = ['env_dataset', 'r2', 'std', 'organ', 'subset' , 'sample_size'])
                df_algo['algo'] = algo_
                list_df.append(df_algo)
            df_all = concat(list_df).reset_index()
            best_idx = df_all.groupby(by = ['env_dataset', 'organ', 'subset'])['r2'].idxmax().reset_index()['r2']
            df  = df_all.loc[best_idx.values]
            df = concat([df, df_heritability])
        if group is not None and group != 'All':
            df  = df[df.subset == group]

        if MODE != 'All':
            df = df[df.organ == MODE]
        df_pivot = pivot_table(df, values = 'r2', index = 'env_dataset', columns = 'organ', dropna = False)
        df_pivot_sample_size = pivot_table(df, values = 'sample_size', index = 'env_dataset', columns = 'organ', dropna = False)
        df_pivot_without_negative = df_pivot.clip(lower = 0)
        d = dict()


        hovertemplate = 'X dataset : %{y}\
                         <br>Organ : %{x}\
                         <br>R2 : %{customdata[0]}\
                         <br>Sample Size : %{customdata[1]}'
        d['data'] = [
            Heatmap(z=df_pivot_without_negative,
                   x=df_pivot_without_negative.columns,
                   y=df_pivot_without_negative.index,
                    #hoverongaps = False,
                    colorscale=get_colorscale(df_pivot_without_negative),
                    customdata = np.dstack([df_pivot.round(4),df_pivot_sample_size]),
                    hovertemplate = hovertemplate,
                    )
            ]


        d2 = dict()
        if view_type == 'Organ':
            d2['data'] = [
                Bar(name = organ, x = df[df.organ == organ].env_dataset, y = df[df.organ == organ].r2, error_y = dict(type = 'data', array = df[df.organ == organ]['std'])) for organ in df.organ.drop_duplicates()
            ]
        elif view_type == 'X':
            d2['data'] = [
                Bar(name = x_dataset, x = df[df.env_dataset == x_dataset].organ, y = df[df.env_dataset == x_dataset].r2, error_y = dict(type = 'data', array = df[df.env_dataset == x_dataset]['std'])) for x_dataset in df.env_dataset.drop_duplicates()
            ]
        d['layout']={'height' : 1000}
        d2['layout'] = {'height' : 1000}

        return Figure(d), Figure(d2)
    else :
        return Figure(empty_graph), Figure(empty_graph)
