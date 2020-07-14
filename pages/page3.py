import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
path_feat_imps = '/Users/samuel/Desktop/dash_app/data/feature_importances_final/'
path_inputs = '/Users/samuel/Desktop/dash_app/data/final_inputs'
list_models = ['Correlation', 'ElasticNet', 'LightGbm', 'NeuralNetwork']
targets = ['Sex', 'Age']
list_organs = [os.path.basename(elem).replace('.csv', '').split('_')[2] for elem in glob.glob(path_feat_imps + '*.csv')]
list_organs = sorted(list(set(list_organs)))

df_sex_age_ethnicity_eid = pd.read_csv('/Users/samuel/Desktop/dash_app/data/sex_age_eid_ethnicity.csv').set_index('id')

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select a target : "),
        dcc.RadioItems(
            id = 'select_target',
            options = get_dataset_options(['Age', 'Sex']),
            value = 'Age',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_1',
            options = get_dataset_options(list_organs),
            value= 'BloodBiochemestry'
            ),
        html.Br()
    ]),
])


table_df = pd.DataFrame(data = {'Corr' : ['Correlation', 'ElasticNet', 'LightGbm', 'NeuralNetwork'],
                                'Correlation' : [1, 0, 0, 0],
                                'ElasticNet' : [0, 1, 0, 0],
                                'LightGbm': [0, 0, 1, 0],
                                'NeuralNetwork' : [0, 0, 0, 1]})

table = dbc.Card([
    dbc.FormGroup([
        html.P("Select correlation type"),
        dcc.RadioItems(
            id = 'select correlation type',
            options = get_dataset_options(['pearson', 'spearman']),
            value = 'pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
        ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Correlation between feature importances/correlation : "),
        dash_table.DataTable(
            id = 'table_corr',
            columns =[{"name": i, "id": i} for i in table_df.columns],
            data = table_df.to_dict('records')
        ),
        html.Br()
    ])
])

layout =  html.Div([
    dcc.Store(id='memory'),
    dcc.Store(id = 'memory_no_str'),
    dcc.Loading([
        dbc.Container([
            dbc.Row([
                dbc.Col([controls,
                         html.Br(),
                         html.Br(),
                         table
                         ], md=4),
                dbc.Col(
                    [dcc.Graph(
                         id='Plot Feature Imps'
                         )
                     ],
                    md=8)
                ])
            ],
            style={"height": "100vh"},
            fluid = True)
        ],
        id = 'Loading Data'
    )])

# @app.callback(Output("Loading Data", "children"),
#               [Input('select_target', 'value'), Input('select_model', 'value'), Input('Select_organ_1', 'value'), Input('select correlation type', 'value')])
# def _ (value_target, value_model, value_organ, corr_type):
#     return value_target, value_model, value_organ, corr_type
#
#
# @app.callback([Output('Plot Feature Imps', 'figure'), Output('table_corr', 'data')],
#               [Input('select_target', 'value'), Input('select_model', 'value'), Input('Select_organ_1', 'value'), Input('select correlation type', 'value')])
# def _plot_r2_scores(value_target, value_model, value_organ, corr_type):
#     if value_model != 'All':
#         df = pd.read_csv(path_feat_imps + 'FeatureImp_%s_%s_%s.csv' % (value_target, value_organ, value_model)).set_index('features')
#         df.columns = [value_model]
#         df = df.sort_values(value_model, ascending = True)
#     else :
#         list_models=['Correlation']
#         list_df = glob.glob(path_feat_imps + 'FeatureImp_%s_%s_*.csv' % (value_target, value_organ))
#         for idx, elem in enumerate(list_df):
#             df_new = pd.read_csv(elem).set_index('features')
#             _, _, _, model = os.path.basename(elem).split('_')
#             model = model.replace('.csv', '')
#             list_models.append(model)
#             df_new.columns = [model]
#             if idx == 0:
#                 df = df_new
#             else :
#                 df = df.join(df_new)
#         df['mean'] = df.mean(axis = 1)
#         df = df.sort_values('mean', ascending = True).drop(columns = ['mean'])
#         df = df/df.sum()
#     features = df.index
#
#     # Add Corr plot
#     df_bio = pd.read_csv(path_inputs + '/%s.csv' % value_organ).set_index('id').dropna()
#     df_corr = df_sex_age_ethnicity_eid.join(df_bio, rsuffix = '_r').dropna()
#     df_corr_age = df_corr['Age when attended assessment centre'].astype('float')
#     features  = ['NA' if pd.isna(elem) else elem for elem in features ]
#     df_corr = df_corr[features].astype('float')
#     corr_with_age = df_corr.apply(lambda col : pearsonr(col, df_corr_age)[0]).abs()
#     corr_with_age = corr_with_age/corr_with_age.sum()
#     corr_with_age.name = 'Correlation'
#     df = df.join(corr_with_age)
#     ## Plot
#     d = {'data' : [go.Bar(name = model, x = df[model], y = df.index, orientation='h') for model in df.columns],
#          'layout' : dict(height = 1000,
#                          margin={'l': 40, 'b': 30, 't': 10, 'r': 0})}
#
#     matrix = df[sorted(list_models)].corr(method=corr_type)
#     matrix.index.name = 'Corr'
#     matrix = matrix.reset_index().round(3)
#
#     return go.Figure(d), matrix.to_dict('records')




@app.callback([Output("Loading Data", "children"), Output("memory", "data"), Output("memory_no_str", "data")],
              [Input('select_target', 'value'), Input('Select_organ_1', 'value')])
def _plot_r2_scores(value_target, value_organ):

    list_models = []
    list_df = glob.glob(path_feat_imps + 'FeatureImp_%s_%s_*.csv' % (value_target, value_organ))
    list_df_sd = glob.glob(path_feat_imps + 'FeatureImp_sd_%s_%s_*.csv' % (value_target, value_organ))

    for idx, elem in enumerate(list_df):
        df_new = pd.read_csv(elem).set_index('features')
        _, _, _, model = os.path.basename(elem).split('_')
        model = model.replace('.csv', '')
        list_models.append(model)
        df_new.columns = [model]
        if idx == 0:
            df = df_new
        else :
            df = df.join(df_new)

    df['mean'] = df.mean(axis = 1)
    df = df.sort_values('mean', ascending = True).drop(columns = ['mean'])
    df = df/df.sum()
    features = df.index

    list_models_sd = []
    for idx, elem in enumerate(list_df_sd):
        df_new_sd = pd.read_csv(elem).set_index('features')
        _, _, _, _, model = os.path.basename(elem).split('_')
        model = model.replace('.csv', '')
        list_models_sd.append(model)
        df_new_sd.columns = [model]
        if idx == 0:
            df_sd = df_new_sd
        else :
            df_sd = df_sd.join(df_new_sd)

    df_sd['mean'] = df_sd.mean(axis = 1)
    df_sd = df_sd.sort_values('mean', ascending = True).drop(columns = ['mean'])
    df_sd = df_sd/df_sd.sum()
    features_sd = df_sd.index

    df_str = df.round(4).astype(str) + ' ± '  + df_sd.round(4).astype(str)
    df.index = df.index.str.replace('.0$', '', regex = True)
    df_str.index = df_str.index.str.replace('.0$', '', regex = True)
    print(df_str)


    # Add Corr plot
    # df_bio = pd.read_csv(path_inputs + '/%s.csv' % value_organ).set_index('id').dropna()
    # df_corr = df_sex_age_ethnicity_eid.join(df_bio, rsuffix = '_r').dropna()
    # df_corr_age = df_corr['Age when attended assessment centre'].astype('float')
    # features  = ['NA' if pd.isna(elem) else elem for elem in features ]
    # df_corr = df_corr[features].astype('float')
    # corr_with_age = df_corr.apply(lambda col : pearsonr(col, df_corr_age)[0]).abs()
    # corr_with_age = corr_with_age/corr_with_age.sum()
    # corr_with_age.name = 'Correlation'
    # df = df.join(corr_with_age).dropna()


    ## Plot
    d = {'data' : [go.Bar(name = model, x = df[model], y = df.index, orientation='h') for model in sorted(df.columns)],
         'layout' : dict(height = len(df.index) * 20,
                         margin={'l': 40, 'b': 30, 't': 10, 'r': 0})}
    matrix = df[sorted(list_models)].corr()
    matrix.index.name = 'Corr'
    matrix = matrix.reset_index().round(3)
    print("Matrix : ", matrix)

    table = dbc.Card([
        dbc.FormGroup([
            html.P("Select correlation type"),
            dcc.RadioItems(
                id = 'select correlation type',
                options = get_dataset_options(['pearson', 'spearman']),
                value = 'pearson',
                labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
            html.Br()
        ]),
        dbc.FormGroup([
            html.P("Correlation between feature importances/correlation : "),
            dash_table.DataTable(
                id = 'table_corr',
                columns =[{"name": i, "id": i} for i in table_df.columns],
                style_cell={'textAlign': 'left'},
                data = matrix.to_dict('records')
            ),
            html.Br()
        ])
    ])

    output = dbc.Container([
        html.H1('Feature Importances'),
        dbc.Row([
            dbc.Col([controls,
                     html.Br(),
                     html.Br(),
                     table
                     ], md=4),
            dbc.Col([
                dash_table.DataTable(
                    id = 'table_feature_imps',
                    columns =[{"name": i, "id": i} for i in ['features'] + sorted(df.columns)],
                    data = df.reset_index().to_dict('records'),
                    style_cell={'textAlign': 'left'},
                    sort_action='custom',
                    sort_mode='single')
                 ],
                style={'overflowY': 'scroll', 'height': 800},
                md=8)
            ],
                className="h-5"),
        html.Br(),
        html.Br(),
        html.H2('Feature Importances - Bar plot'),
        html.Br(),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Graph(
                     id='Plot Feature Imps',
                     figure = go.Figure(d)
                     )
            ],
            style={'overflowY': 'scroll', 'height' : 1500},
            width={"size": 10, "offset": 1})
        ], className="h-75")
        ],
        style={"height": "100vh"},
        fluid = True)
    print([{"name": i, "id": i} for i in df.reset_index().columns])

    return output, df_str.to_dict(), df.to_dict()




@app.callback(Output('table_feature_imps', 'data'),
              [Input('table_feature_imps', 'sort_by'), Input('memory', 'data')])

def _sort_table(sort_by_col, data):
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    df.index.name = 'features'
    df = df.reset_index()
    if sort_by_col is not None and len(sort_by_col):
        sorting = sort_by_col[0]
        ascending = (sorting['direction'] == 'asc')
        df = df.sort_values(sorting['column_id'], ascending = ascending)
    df = df.round(5)
    return df.to_dict('records')


@app.callback(Output('table_corr', 'data'),
              [Input('select correlation type', 'value'), Input('memory_no_str', 'data')])
def _change_corr_method(value, data):
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    corr_matrix = df.corr(method=value)
    corr_matrix.index.name = 'Corr'
    corr_matrix = corr_matrix.reset_index().round(3)
    return corr_matrix.to_dict('record')
