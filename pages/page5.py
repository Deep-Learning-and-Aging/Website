import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, empty_graph, load_csv
from pandas import concat, Index, DataFrame
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
from botocore.exceptions import ClientError
from app import app, MODE
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
organs = sorted([ "*", "*instances01", "*instances1.5x", "*instances23", "Abdomen", "AbdomenLiver", "AbdomenPancreas", "Arterial", "ArterialPulseWaveAnalysis", "ArterialCarotids", "Biochemistry", "BiochemistryUrine", "BiochemistryBlood", "Brain", "BrainCognitive", "BrainMRI", "Eyes", "EyesAll" ,"EyesFundus", "EyesOCT", "Hearing", "HeartMRI", "Heart", "HeartECG", "ImmuneSystem", "Lungs", "Musculoskeletal", "MusculoskeletalSpine", "MusculoskeletalHips", "MusculoskeletalKnees", "MusculoskeletalFullBody", "MusculoskeletalScalars", "PhysicalActivity" ])

path_linear_ewas = 'page5_LinearXWASResults/LinearOutput/'
Environmental = sorted(['All', 'Alcohol', 'Diet', 'Education', 'ElectronicDevices',
                 'Employment', 'FamilyHistory', 'Eyesight', 'Mouth',
                 'GeneralHealth', 'Breathing', 'Claudification', 'GeneralPain',
                 'ChestPain', 'CancerScreening', 'Medication', 'Hearing',
                 'Household', 'MentalHealth', 'OtherSociodemographics',
                 'PhysicalActivity', 'SexualFactors', 'Sleep', 'SocialSupport',
                 'SunExposure', 'EarlyLifeFactors'])
Biomarkers = sorted(['All', 'HandGripStrength', 'BrainGreyMatterVolumes', 'BrainSubcorticalVolumes',
              'HeartSize', 'HeartPWA', 'ECGAtRest', 'AnthropometryImpedance',
              'UrineBiochemestry', 'BloodBiochemestry', 'BloodCount',
              'EyeAutorefraction', 'EyeAcuity', 'EyeIntraoculaPressure',
              'BraindMRIWeightedMeans', 'Spirometry', 'BloodPressure',
              'AnthropometryBodySize', 'ArterialStiffness', 'CarotidUltrasound',
              'BoneDensitometryOfHeel', 'HearingTest'])
Pathologies = sorted(['All'] + ['medical_diagnoses_%s' % letter for letter in ['A', 'B', 'C', 'D', 'E',
                                                    'F', 'G', 'H', 'I', 'J',
                                                    'K', 'L', 'M', 'N', 'O',
                                                    'P', 'Q', 'R', 'S', 'T',
                                                    'U', 'V', 'W', 'X', 'Y', 'Z']])
All = sorted(list(set(Environmental + Biomarkers + Pathologies)))

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select data type: "),
        dcc.RadioItems(
            id='Select_data_type',
            options = get_dataset_options(['All', 'Biomarkers', 'Pathologies', 'Environmental']),
            value = 'All',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ], id = 'Select_data_type_full'),
    dbc.FormGroup([
        html.P("Select X Dataset : "),
        dcc.Dropdown(
            id='Select_dataset_ewas',
            options = [{'value' : '', 'label' : ''}],
            placeholder = 'All',
            value = 'All',
            multi=True
            ),
        html.Br()
    ], id = 'Select_dataset_ewas_full'),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_ewas',
            options = get_dataset_options(organs),
            value = 'Heart'
            ),
        html.Br()
    ], id = 'Select_organ_ewas_full'),
])


if MODE != 'All':
    organs = [MODE]
    controls = dbc.Card([
        dbc.FormGroup([
            html.P("Select data type: "),
            dcc.RadioItems(
                id='Select_data_type',
                options = get_dataset_options(['All', 'Biomarkers', 'Pathologies', 'Environmental']),
                value = 'All',
                labelStyle = {'display': 'inline-block', 'margin': '5px'}
                ),
            html.Br()
        ], id = 'Select_data_type_full'),
        dbc.FormGroup([
            html.P("Select X Dataset : "),
            dcc.Dropdown(
                id='Select_dataset_ewas',
                options = [{'value' : '', 'label' : ''}],
                placeholder = 'All',
                value = 'All',
                multi=True
                ),
            html.Br()
        ], id = 'Select_dataset_ewas_full'),
        dbc.FormGroup([
            html.P("Select an Organ : "),
            dcc.Dropdown(
                id='Select_organ_ewas',
                options = get_dataset_options([MODE]),
                value = MODE
                ),
            html.Br()
        ], id = 'Select_organ_ewas_full', style = {'display' : 'None'}),

    ])


@app.callback(Output('Select_dataset_ewas', 'options'),
              [Input('Select_data_type', 'value')])
def _select_sub_dropdown(val_data_type):
    if val_data_type == 'All':
        return get_dataset_options(All)
    elif val_data_type == 'Environmental':
        return get_dataset_options(Environmental)
    elif val_data_type == 'Biomarkers':
        return get_dataset_options(Biomarkers)
    elif val_data_type == 'Pathologies':
        return get_dataset_options(Pathologies)


layout = dbc.Container([
                html.H1('Univariate XWAS - Results'),
                html.Br(),
                html.Br(),
                dcc.Loading([
                    dbc.Row([
                        dbc.Col([controls,
                                 html.Br(),
                                 html.Br()], md=3),
                        dbc.Col(
                            [dcc.Store(id='memory_ewas'),
                            dcc.Graph(
                             id='Volcano Plot - EWAS'
                             )
                            ],
                            md=9)
                            ]),
                    dbc.Row([
                        dbc.Col([
                            dash_table.DataTable(
                                id = 'table_ewas_linear',
                                columns =[{"name": i, "id": i} for i in ['Environmental Feature', 'Organ', 'X Dataset', 'p_value', 'Partial correlation', 'Sample Size']],
                                style_cell={'textAlign': 'left'},
                                sort_action='custom',
                                sort_mode='single')
                                ],
                        #style={'overflowY': 'scroll', 'height': 2000},
                        width={"size": 8, "offset": 3}
                        )
                    ])
                ])
            ],
            fluid = True
        )



@app.callback([Output('Volcano Plot - EWAS', 'figure'), Output('memory_ewas', 'data')],
              [Input('Select_organ_ewas', 'value'), Input('Select_data_type', 'value'), Input('Select_dataset_ewas', 'value')])
def _modify_ewas_volcano_plot(value_organ, value_data, value_datasets):
    fig = {'layout' : dict(title='Volcano plot', # title of plot
                           xaxis_title='Partial correlation',
                           yaxis_title='-log(p_value)'
                           )}
    data = None
    if value_organ is not None and value_data is not None:
        list_df = []
        for idx, env_dataset in enumerate(globals()[value_data]):
            try :
                if value_organ == '*':
                    value_organ = '\\*'
                t = load_csv(path_linear_ewas + 'linear_correlations_%s_%s.csv' % (env_dataset, value_organ))
                t['Env_Dataset'] = env_dataset
                list_df.append(t)
                if value_organ == '\\*':
                    value_organ = '*'
            except (FileNotFoundError, ClientError):
                continue

        if len(list_df) == 0:
            return Figure(empty_graph), {}
        res = concat(list_df)
        res['p_val'] = res['p_val'].replace(0, 1e-323)
        res['env_feature_name'] = res['env_feature_name'].str.replace('.0', '')

        if value_datasets != 'All' or value_datasets is None:
            res = res[res.Env_Dataset.isin(value_datasets)]

        hovertemplate = 'Feature : %{customdata[0]}\
                         <br>Organ : %{customdata[1]}\
                         <br>X Dataset : %{customdata[2]}\
                         <br>p_value : %{customdata[3]:.3E}\
                         <br>Partial correlation : %{customdata[4]:.3f}\
                         <br>Sample Size : %{customdata[5]}'

        fig['data'] = []
        for env_dataset in res.Env_Dataset.drop_duplicates():
            res_ = res[res.Env_Dataset == env_dataset]
            customdata = np.stack([res_['env_feature_name'], res_['target_dataset_name'], res_['Env_Dataset'], res_['p_val'], res_['corr_value'], res_['size_na_dropped']], axis=-1)
            fig['data'].append(
                Scatter(x = res_['corr_value'],
                           y = -np.log10(res_['p_val']),
                           mode='markers',
                           name = env_dataset,
                           hovertemplate = hovertemplate,
                           customdata=customdata))
        num_tests = res.shape[0]
        shapes = []
        line = dict(
            color="Black",
            width=0.5
                  )
        fig['data'].append(
            Scatter(x = [res['corr_value'].min() - res['corr_value'].std(), res['corr_value'].max() + res['corr_value'].std()],
                       y = [-np.log((5/100)), -np.log((5/100))],
                       name = 'No Correction',
                       mode = 'lines'))
        fig['data'].append(
            Scatter(x = [res['corr_value'].min() - res['corr_value'].std(), res['corr_value'].max() + res['corr_value'].std()],
                       y = [-np.log((5/100)/num_tests), -np.log((5/100)/num_tests)],
                       name = 'With Bonferoni Correction',
                       mode = 'lines'))

        data = res.rename(columns = dict(zip(['env_feature_name', 'target_dataset_name', 'Env_Dataset', 'p_val', 'corr_value', 'size_na_dropped'],
                                             ['Environmental Feature', 'Organ', 'X Dataset', 'p_value', 'Partial correlation', 'Sample Size']))).to_dict('records')
    return Figure(fig), data


@app.callback(Output('table_ewas_linear', 'data'),
              [Input('table_ewas_linear', 'sort_by'), Input('memory_ewas', 'data'), Input('Volcano Plot - EWAS', 'restyleData')])
def _sort_table(sort_by_col, data, restyle):
    df = DataFrame(data = data)
    df = df.reset_index()
    if sort_by_col is not None and len(sort_by_col):
        sorting = sort_by_col[0]
        ascending = (sorting['direction'] == 'asc')
        df = df.sort_values(sorting['column_id'], ascending = ascending)
    df = df.round(5)
    return df.to_dict('records')
