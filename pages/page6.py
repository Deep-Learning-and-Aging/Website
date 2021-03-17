import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, empty_graph, load_csv
from pandas import pivot_table
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
from plotly.subplots import make_subplots
from app import app
import glob
import plotly.figure_factory as ff
from scipy.spatial.distance import squareform
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
organs = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])

path_correlations_ewas = 'page6_LinearXWASCorrelations/CorrelationsLinear/'
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
              'BoneDensitometryOfHeel', 'HearingTest', 'CognitiveFluidIntelligence',
              'CognitiveMatrixPatternCompletion', 'CognitiveNumericMemory', 'CognitivePairedAssociativeLearning',
              'CognitivePairsMatching', 'CognitiveProspectiveMemory', 'CognitiveReactionTime',
              'CognitiveSymbolDigitSubstitution', 'CognitiveTowerRearranging', 'CognitiveTrailMaking'])
Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = sorted(Environmental + Biomarkers + Pathologies)

colorscale =  [[0, 'rgba(255, 0, 0, 0.85)'],
               [0.5, 'rgba(255, 255, 255, 0.85)'],
               [1, 'rgba(0, 0, 255, 0.85)']]

controls1 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_lin_ewas1',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_subset_method1',
            options = get_dataset_options(['All', 'Union', 'Intersection']),
            value = 'Union',
            )
    ]),
    dbc.FormGroup([
        html.P("Select X Dataset: "),
        dcc.Dropdown(
            id='Select_env_dataset_lin_ewas',
            options = get_dataset_options(sorted(All)),
            value = sorted(All)[0]
            ),
        html.Br()
        ], id = 'Select_env_dataset_lin_ewas_full')
])

controls2 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_lin_ewas2',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_subset_method2',
            options = get_dataset_options(['All', 'Union', 'Intersection']),
            placeholder = 'All',
            value = 'All',
            )
    ]),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_lin_ewas',
            options = get_dataset_options(organs),
            value = sorted(organs)[0],
            ),
        html.Br()
        ], id = 'Select_organ_lin_ewas_full')
])

layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label = 'Select X', tab_id='tab_X'),
        dbc.Tab(label = 'Select Organ', tab_id = 'tab_organ'),
    ], id = 'tab_manager', active_tab = 'tab_X'),
    html.Div(id="tab-content")
])


@app.callback(Output('tab-content', 'children'),
             [Input('tab_manager', 'active_tab')])
def _plot_with_given_env_dataset(ac_tab):
    if ac_tab == 'tab_X':
        return  dbc.Container([
                        html.H1('Univariate XWAS - Correlations'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([

                            dbc.Col([controls1,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    html.H2(id = 'scores_univ_xwas_X'),
                                    dcc.Graph(id='Correlation - Select Ewas dataset')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)
    elif ac_tab == 'tab_organ':
        return  dbc.Container([
                        html.H1('Univariate XWAS - Correlations'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([

                            dbc.Col([controls2,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    html.H2(id = 'scores_univ_xwas_organ'),
                                    dcc.Graph(id='Correlation - Select Organ')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)


@app.callback([Output('Correlation - Select Organ', 'figure'),
               Output('scores_univ_xwas_organ', 'children')],
             [Input('Select_corr_type_lin_ewas2', 'value'),
              Input('Select_subset_method2', 'value'),
              Input('Select_organ_lin_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, organ):
    if corr_type is not None and subset_method is not None:
        df = load_csv(path_correlations_ewas + 'Correlations_%s_%s.csv' % (subset_method, corr_type)).replace('\\*', '*')
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr', 'sample_size']]
        df_organ = df[df.organ_1 == organ]
        df_organ = df_organ[df_organ.organ_2 != organ]
        df_organ = df_organ.fillna(0)

        matrix_organ = pivot_table(df_organ, values='corr', index=['env_dataset'],
                        columns=['organ_2'])

        try :
            colorscale = get_colorscale(matrix_organ)
        except ValueError:
            return Figure(empty_graph)
        d = {}
        sample_size_matrix =  pivot_table(df_organ, values='sample_size', index=['env_dataset'],
                columns=['organ_2']).values
        matrix_organ[sample_size_matrix < 10] = 0
        customdata = np.dstack((sample_size_matrix, matrix_organ))
        title = "Average correlation = %.3f ± %.3f" % (np.mean(matrix_organ.values.flatten()), np.std(matrix_organ.values.flatten()))
        hovertemplate = 'Correlation : %{z}\
                 <br>Organ x : %{x}\
                 <br>Organ y : %{y}\
                 <br>Sample Size : %{customdata[0]}'

        d['data'] = Heatmap(z=matrix_organ.T,
                   x=matrix_organ.T.columns,
                   y=matrix_organ.T.index,
                   colorscale = colorscale,
                   customdata = customdata,
                   hovertemplate = hovertemplate)

        d['layout'] = dict(xaxis = dict(dtick = 1),
                           yaxis = dict(dtick = 1),
                           width = 1000,
                           height = 600)
        return Figure(d), title
    else :
        return Figure(), ''


@app.callback([Output('Correlation - Select Ewas dataset', 'figure'), Output('scores_univ_xwas_X', 'children')],
             [Input('Select_corr_type_lin_ewas1', 'value'), Input('Select_subset_method1', 'value'), Input('Select_env_dataset_lin_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, env_dataset):
    if corr_type is not None and subset_method is not None:
        df = load_csv(path_correlations_ewas + 'Correlations_%s_%s.csv' % (subset_method, corr_type)).replace('\\*', '*')
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr', 'sample_size']]
        df_env = df[df.env_dataset == env_dataset]
        df_env = df_env.fillna(0)

        sample_size_matrix = pivot_table(df_env, values='sample_size', index=['organ_1'], columns=['organ_2'])

        env_matrix = pivot_table(df_env, values='corr', index=['organ_1'], columns=['organ_2'])
        env_matrix[sample_size_matrix < 10] = 0
        labels = env_matrix.columns 

        fig = ff.create_dendrogram(env_matrix, orientation="bottom",distfun=lambda df: 1 - df)
        for scatter in fig['data']:
            scatter['yaxis'] = 'y2'

        order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))

        fig.update_layout(xaxis={"ticktext": labels[order_dendrogram], "mirror": False})
        fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})


        heat_data = env_matrix.values[order_dendrogram,:]
        heat_data = heat_data[:,order_dendrogram]
        try :
            colorscale =  get_colorscale(heat_data)
        except ValueError:
            return Figure(empty_graph)

        heat_data = env_matrix.values[order_dendrogram,:]
        heat_data = heat_data[:,order_dendrogram]
        colorscale =  get_colorscale(heat_data)

        heat_sample_size = sample_size_matrix.values[order_dendrogram,:]
        heat_sample_size = heat_sample_size[:,order_dendrogram]
        customdata = np.dstack((heat_sample_size, heat_data))
        hovertemplate = 'Correlation : %{z}\
                            <br>Organ x : %{x}\
                            <br>Organ y : %{y}\
                            <br>Sample Size : %{customdata[0]}'
        idx_upper = np.triu_indices(len(heat_data))
        title = "Average correlation = %.3f ± %.3f" % (np.mean(heat_data[idx_upper]), np.std(heat_data[idx_upper]))

        heatmap = Heatmap(
                x = labels[order_dendrogram],
                y = labels[order_dendrogram],
                z = heat_data,
                colorscale = colorscale,
                customdata = customdata,
                hovertemplate = hovertemplate
            )

        heatmap['x'] = fig['layout']['xaxis']['tickvals']
        heatmap['y'] = fig['layout']['xaxis']['tickvals']

        fig.update_layout(yaxis={'domain': [0, .85], 'mirror': False, 'showgrid': False, 'zeroline': False, 'ticktext': labels[order_dendrogram], "tickvals":fig['layout']['xaxis']['tickvals'], 'showticklabels': True, "ticks": "outside"})

        fig.add_trace(heatmap)

        fig['layout']['width'] = 1100
        fig['layout']['height'] = 1100

        return fig, title  # Figure(d), title
    else:
        return Figure(), ''
