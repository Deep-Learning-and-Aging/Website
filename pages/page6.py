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
import pandas as pd
from scipy.stats import pearsonr
import dash_table
import copy
organs = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])


Old_Environmental = sorted(['Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivity', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors', 'Smoking'])
Old_Biomarkers = sorted(['HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemistry', 'BloodBiochemistry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraocularPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest', 'CognitiveFluidIntelligence',
              'CognitiveMatrixPatternCompletion', 'CognitiveNumericMemory', 'CognitivePairedAssociativeLearning',
              'CognitivePairsMatching', 'CognitiveProspectiveMemory', 'CognitiveReactionTime',
              'CognitiveSymbolDigitSubstitution', 'CognitiveTowerRearranging', 'CognitiveTrailMaking'])
Old_Pathologies = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]
All = sorted(Old_Environmental + Old_Biomarkers + Old_Pathologies)


path_correlations_ewas = 'page6_LinearXWASCorrelations/CorrelationsLinear/'
Environmental = sorted(["Alcohol", "Diet", "EarlyLifeFactors", "ElectronicDevices", "Medication", "SunExposure", "Smoking"])
Socioeconomics = sorted(["Education", "Employment", "Household", "SocialSupport", "OtherSociodemographics"])
Phenotypes = sorted(["Breathing", "CancerScreening", "ChestPain", "Claudication", "Eyesight", "GeneralHealth", "GeneralPain", "Hearing", "MentalHealth", "Mouth", "SexualFactors", "Sleep"])
OtherSociodemographics = ["FamilyHistory"]
Diseases = ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']]

colorscale =  [[0, 'rgba(255, 0, 0, 0.85)'],
               [0.5, 'rgba(255, 255, 255, 0.85)'],
               [1, 'rgba(0, 0, 255, 0.85)']]

controls1 = dbc.Card([
    dbc.FormGroup([
        html.P("Select data type: "),
        dcc.RadioItems(
            id='Select_data_type',
            options = get_dataset_options(['All', 'Environmental', 'Socioeconomics', 'Phenotypes', 'OtherSociodemographics', 'Diseases']),
            value = 'All',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ], id = 'Select_data_type_full'),
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
            options = [{'value' : '', 'label' : ''}],
            placeholder = 'All',
            value = 'All',
            ),
        html.Br()
        ], id = 'Select_env_dataset_lin_ewas_full')
])

@app.callback(Output('Select_env_dataset_lin_ewas', 'options'),
              [Input('Select_data_type', 'value')])
def _select_sub_dropdown(val_data_type):
    if val_data_type == 'All':
        return get_dataset_options(All) + [{'value': 'All', 'label': 'All'}]
    elif val_data_type == 'Environmental':
        return get_dataset_options(Environmental) + [{'value': 'Environmental', 'label': 'All'}]
    elif val_data_type == 'Socioeconomics':
        return get_dataset_options(Socioeconomics) + [{'value': 'Socioeconomics', 'label': 'All'}]
    elif val_data_type == 'Phenotypes':
        return get_dataset_options(Phenotypes) + [{'value': 'Phenotypes', 'label': 'All'}]
    elif val_data_type == 'OtherSociodemographics':
        return get_dataset_options(OtherSociodemographics) + [{'value': 'OtherSociodemographics', 'label': 'All'}]
    else:  # val_data_type == 'Diseases':
        return get_dataset_options(Diseases) + [{'value': 'Diseases', 'label': 'All'}]
    

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

controls3 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_lin_ewas3',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_subset_method3',
            options = get_dataset_options(['All', 'Union', 'Intersection']),
            value = 'Union',
            )
    ]),
])

layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label = 'Select X', tab_id='tab_X'),
        dbc.Tab(label = 'Select Organ', tab_id = 'tab_organ'),
        dbc.Tab(label = 'Select Average', tab_id = 'tab_average')
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
    else:  # ac_tab == "tab_average"
        return  dbc.Container([
                        html.H1('Univariate XWAS - Correlations'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls3,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    html.H2(id = 'scores_univ_xwas_average'),
                                    dcc.Graph(id='Correlation - Select Average')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)



@app.callback([Output('Correlation - Select Average', 'figure'),
               Output('scores_univ_xwas_average', 'children')],
             [Input('Select_corr_type_lin_ewas3', 'value'),
              Input('Select_subset_method3', 'value')])
def _plot_with_average_correlation(corr_type, subset_method):
    data = load_csv(path_correlations_ewas + 'Correlations_%s_%s.csv' % (subset_method, corr_type)).replace('\\*', '*')
    correlation_data = pd.DataFrame(None, index=All + ["All", "Environmental", "Socioeconomics", "Phenotypes", "Diseases"], columns=["mean", "std"])

    all_correlations = []

    def fill_correlations(df):
        correlation_data.loc[df.env_dataset.tolist()[0], "mean"] = np.round_(np.mean(df["corr"]), 3)
        correlation_data.loc[df.env_dataset.tolist()[0], "std"] = np.round_(np.std(df["corr"]), 3)
        
        all_correlations.append(df["corr"].reset_index(drop=True))

    data.groupby(by="env_dataset").apply(fill_correlations)

    concat_all_correlations = pd.concat(all_correlations)
    title = f"Average correlations per X dataset \n Average : {np.round_(np.mean(concat_all_correlations), 3)} +- {np.round_(np.std(concat_all_correlations), 3)}"
    
    correlation_data.sort_values(by="mean", ascending=False, inplace=True)
    
    fig = Figure()
    fig.add_trace(
        Bar(
            x=correlation_data.index,
            y=correlation_data["mean"],
            error_y={"array": correlation_data["std"], "type": "data"},
            name="Average correlations",
            marker_color="indianred",
        )
    )
    fig.update_layout(xaxis_tickangle=-90)
    fig.update_layout({"width": 1800, "height": 600})

    return fig, title



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

        heat_sample_size = sample_size_matrix.values[order_dendrogram,:]
        heat_sample_size = heat_sample_size[:,order_dendrogram]
        customdata = np.dstack((heat_sample_size, heat_data))
        hovertemplate = 'Correlation : %{z}\
                            <br>Organ x : %{x}\
                            <br>Organ y : %{y}\
                            <br>Sample Size : %{customdata[0]}'
        idx_upper = np.triu_indices(len(heat_data))
        title = "Average correlation = %.3f ± %.3f" % (np.mean(heat_data), np.std(heat_data))

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
