import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, empty_graph, load_csv
from pandas import pivot_table
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
import plotly.figure_factory as ff
from app import app
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr
import dash_table
import copy



organs = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])

path_scores_ewas = 'page7_MultivariateXWASResults/Scores/'
path_correlations_ewas = 'page8_MultivariateXWASCorrelations/CorrelationsMultivariate/'
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
#     d['data'] = Heatmap(z=matrix_env,
#                x=matrix_env.index,
#                y=matrix_env.columns,
#                colorscale = colorscale)
#     d['layout'] = dict(xaxis = dict(dtick = 1),
#                        yaxis = dict(dtick = 1),
#                        width = 600,
#                        height = 600)
#
#     return Figure(d)
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
#     d['data'] = Heatmap(z=matrix_organ.T,
#                x=matrix_organ.T.columns,
#                y=matrix_organ.T.index,
#                colorscale = colorscale)
#     d['layout'] = dict(xaxis = dict(dtick = 1),
#                        yaxis = dict(dtick = 1),
#                        width = 1000,
#                        height = 600)
#     return Figure(d)




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
        html.P("Select X Dataset: "),
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

controls3 = dbc.Card([
    dbc.FormGroup([
        dbc.Label("Select correlation type :"),
        dcc.RadioItems(
            id='Select_corr_type_mul_ewas3',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            )
    ]),
    dbc.FormGroup([
        dbc.Label("Select subset method :"),
        dcc.Dropdown(
            id='Select_algorithm_method3',
            options = get_dataset_options(['LightGbm', 'ElasticNet', 'NeuralNetwork']),
            placeholder = 'LightGbm',
            value = 'LightGbm',
            )
    ]),
])

layout = html.Div([
    dbc.Tabs([
        dbc.Tab(label = 'Select X', tab_id='tab_X'),
        dbc.Tab(label = 'Select Organ', tab_id = 'tab_organ'),
        dbc.Tab(label = 'Select Organ', tab_id = 'tab_average'),
    ], id = 'tab_manager_mul', active_tab = 'tab_average'),
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
    else:  # ac_tab == 'tab_average'
        return  dbc.Container([
                        html.H1('Multivariate XWAS - Correlations between accelerated aging'),
                        html.Br(),
                        html.Br(),
                        dbc.Row([
                            dbc.Col([controls3,
                                     html.Br(),
                                     html.Br()], md=3),
                            dbc.Col(
                                [dcc.Loading([
                                    html.H2(id = 'title_average'),
                                    dcc.Graph(id='Correlation Mul - Select Average')
                                 ])],
                                style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                                md=9)
                                ])
                        ], fluid = True)

@app.callback([Output('Correlation Mul - Select Average', 'figure'), Output('title_average', 'children')],
            [Input('Select_corr_type_mul_ewas3', 'value'), Input('Select_algorithm_method3', 'value')])
def _plot_with_average_dataset(corr_type, algo):
    data = load_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, algo))
    data['env_dataset'] = data['env_dataset'].str.replace('Clusters_', '')
    data.loc[data.sample_size < 10, 'corr'] = 0
    correlation_data = pd.DataFrame(None, index=data.env_dataset.drop_duplicates(), columns=["mean", "std"])
    all_correlations = []

    def fill_correlations(df):
        correlation_data.loc[df.env_dataset.tolist()[0], "mean"] = np.round_(np.mean(df["corr"]), 3)
        correlation_data.loc[df.env_dataset.tolist()[0], "std"] = np.round_(np.std(df["corr"]), 3)
        
        all_correlations.append(df["corr"].reset_index(drop=True))

    data.groupby(by="env_dataset").apply(fill_correlations)

    concat_all_correlations = pd.concat(all_correlations)
    title = f"Average correlations per X dataset \n Average : {np.round_(np.mean(concat_all_correlations), 3)} +- {np.round_(np.std(concat_all_correlations), 3)}"

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
    fig.update_layout({"width": 1400, "height": 600})
    return fig, title


@app.callback(Output('Correlation Mul - Select Ewas dataset', 'figure'),
             [Input('Select_corr_type_mul_ewas1', 'value'), Input('Select_algorithm_method1', 'value'), Input('Select_env_dataset_mul_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, env_dataset):
    if corr_type is not None and subset_method is not None:
        score = load_csv(path_scores_ewas + 'Scores_EWAS.csv')
        score['env_dataset'] = score['env_dataset'].str.replace('Clusters_', '')
        distinct_organs = score.organ.drop_duplicates()
        score_std_env = score[score['env_dataset']== env_dataset][['r2', 'organ', 'std']]
        score_env = dict(zip(score_std_env['organ'], score_std_env['r2']))
        std_env = dict(zip(score_std_env['organ'], score_std_env['std']))
        for organ in distinct_organs:
            if organ not in score_env.keys():
                score_env[organ] = np.nan
            if organ not in std_env.keys():
                std_env[organ] = np.nan
        df = load_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, subset_method))
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
        df['env_dataset'] = df['env_dataset'].str.replace('Clusters_', '')
        df_env = df[df.env_dataset == env_dataset]
        #df_env = df_env.merge(score, how = 'inner', left_on = 'organ_1', right_on = 'organ')
        df_env['score_1'] = df_env['organ_1'].map(score_env)
        df_env['score_2'] = df_env['organ_2'].map(score_env)
        df_env['std_1'] = df_env['organ_1'].map(std_env)
        df_env['std_2'] = df_env['organ_2'].map(std_env)

        env_matrix = pivot_table(df_env, values='corr', index=['organ_1'],
                        columns=['organ_2'], dropna = False)
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

        r2_score_y = pivot_table(df_env, values='score_1', index=['organ_1'],
                        columns=['organ_2'], dropna = False)
        r2_score_y = r2_score_y.values[order_dendrogram,:]
        r2_score_y = r2_score_y[order_dendrogram,:]
        r2_score_x = pivot_table(df_env, values='score_2', index=['organ_1'],
                        columns=['organ_2'], dropna = False)
        r2_score_x = r2_score_x.values[order_dendrogram,:]
        r2_score_x = r2_score_x[:,order_dendrogram]
        std_y = pivot_table(df_env, values='std_1', index=['organ_1'],
                        columns=['organ_2'], dropna = False)
        std_y = std_y.values[order_dendrogram,:]
        std_y = std_y[:,order_dendrogram]
        std_x = pivot_table(df_env, values='std_2', index=['organ_1'],
                        columns=['organ_2'], dropna = False)
        std_x = std_x.values[order_dendrogram,:]
        std_x = std_x[:,order_dendrogram]
        
        customdata = np.dstack((r2_score_x, std_x, r2_score_y, std_y))
        hovertemplate = "Organ x : %{x}<br> Score organ x : %{customdata[0]:.3f}<br>Std organ y : %{customdata[1]:.3f}<br>Organ y : %{y}<br>Score organ y : %{customdata[2]:.3f}<br>Std organ y : %{customdata[3]:.3f}"

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
        return fig
    else:
        return Figure()



@app.callback(Output('Correlation Mul - Select Organ', 'figure'),
             [Input('Select_corr_type_mul_ewas2', 'value'), Input('Select_algorithm_method2', 'value'), Input('Select_organ_mul_ewas', 'value')])
def _plot_with_given_organ_dataset(corr_type, subset_method, organ):
    if corr_type is not None and subset_method is not None:
        score = load_csv(path_scores_ewas + 'Scores_EWAS.csv')
        score['env_dataset'] = score['env_dataset'].str.replace('Clusters_', '')
        distinct_organs = score.organ.drop_duplicates()
        score_std_organ = score[score['organ']== organ][['r2', 'organ', 'std', 'env_dataset']]
        score_org = dict(zip(score_std_organ['env_dataset'], score_std_organ['r2']))
        std_org = dict(zip(score_std_organ['env_dataset'], score_std_organ['std']))
        score_env = dict(zip(score_std_organ['organ'], score_std_organ['r2']))
        std_env = dict(zip(score_std_organ['organ'], score_std_organ['std']))
        for organ in distinct_organs:
            if organ not in score_org.keys():
                score_env[organ] = np.nan
            if organ not in std_org.keys():
                std_env[organ] = np.nan
        df = load_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, subset_method))
        df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
        df['env_dataset'] = df['env_dataset'].str.replace('Clusters_', '')
        df_org = df[df.organ_2 == organ]
        #df_env = df_env.merge(score, how = 'inner', left_on = 'organ_1', right_on = 'organ')
        df_org['score_1'] = df_org['organ_1'].map(score_org)
        df_org['score_env'] = df_org['env_dataset'].map(score_env)
        df_org['std_1'] = df_org['organ_1'].map(std_org)
        df_org['std_env'] = df_org['env_dataset'].map(std_env)

        matrix_org = pivot_table(df_org, values='corr', index=['organ_1'],
                        columns=['env_dataset'], dropna = False)
        r2_score_y = pivot_table(df_org, values='score_1', index=['organ_1'],
                        columns=['env_dataset'], dropna = False)
        r2_score_x = pivot_table(df_org, values='score_env', index=['organ_1'],
                        columns=['env_dataset'], dropna = False)
        std_y = pivot_table(df_org, values='std_1', index=['organ_1'],
                        columns=['env_dataset'], dropna = False)
        std_x = pivot_table(df_org, values='std_env', index=['organ_1'],
                        columns=['env_dataset'], dropna = False)
        customdata = np.dstack((r2_score_x, std_x, r2_score_y, std_y))
        hovertemplate = "Organ x : %{x}<br> Score organ x : %{customdata[0]:.3f}<br>Std organ y : %{customdata[1]:.3f}<br>Organ y : %{y}<br>Score organ y : %{customdata[2]:.3f}<br>Std organ y : %{customdata[3]:.3f}"
        try :
            colorscale =  get_colorscale(matrix_org)
        except ValueError:
            return Figure(empty_graph)
        d = {}
        d['data'] = Heatmap(z=matrix_org,
                   x=matrix_org.index,
                   y=matrix_org.columns,
                   customdata =customdata,
                   hovertemplate = hovertemplate,
                   colorscale = colorscale)
        d['layout'] = dict(xaxis = dict(dtick = 1),
                           yaxis = dict(dtick = 1),
                           width = 800,
                           height = 800)
        return Figure(d)
    else:
        return Figure()

# @app.callback(Output('Correlation Mul - Select Organ', 'figure'),
#              [Input('Select_corr_type_mul_ewas2', 'value'), Input('Select_algorithm_method2', 'value'), Input('Select_organ_mul_ewas', 'value')])
# def _plot_with_given_organ_dataset(corr_type, subset_method, organ):
#     if corr_type is not None and subset_method is not None:
#         df = load_csv(path_correlations_ewas + 'CorrelationsMultivariate_%s_%s.csv' % (corr_type, subset_method))
#         df = df[['env_dataset', 'organ_1', 'organ_2', 'corr']]
#         df['env_dataset'] = df['env_dataset'].str.replace('Clusters_', '')
#         df_organ = df[df.organ_1 == organ]
#         df_organ = df_organ[df_organ.organ_2 != organ]
#         matrix_organ = pivot_table(df_organ, values='corr', index=['env_dataset'],
#                         columns=['organ_2'])
#         try :
#             colorscale =  get_colorscale(matrix_organ)
#         except ValueError:
#             return Figure(empty_graph)
#         d = {}
#         d['data'] = Heatmap(z=matrix_organ.T,
#                    x=matrix_organ.T.columns,
#                    y=matrix_organ.T.index,
#                    colorscale = colorscale)
#         d['layout'] = dict(xaxis = dict(dtick = 1),
#                            yaxis = dict(dtick = 1),
#                            width = 1000,
#                            height = 800)
#         return Figure(d)
#     else :
#         return Figure()
