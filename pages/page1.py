import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import glob
import os
from sklearn.linear_model import LinearRegression
import time
import numpy as np
from scipy.stats import pearsonr, linregress

from .tools import get_dataset_options, ETHNICITY_COLS

from app import app
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots

path_inputs = '/Users/samuel/Desktop/dash_app/data/final_inputs'
path_biomarkers = '/Users/samuel/Desktop/dash_app/data/Biomarkers_raw.csv'
path_linear = '/Users/samuel/Desktop/dash_app/data/LinearOutput/'

df_sex_age_ethnicity_eid = pd.read_csv('/Users/samuel/Desktop/dash_app/data/data/sex_age_eid_ethnicity.csv').set_index('id')
biomarkers_groups = [os.path.basename(elem).replace('.csv', '') for elem in glob.glob(path_inputs + '/*.csv')]


controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select Dataset : "),
        dcc.Dropdown(
            id = 'select_group_biomarkers',
            options = get_dataset_options(biomarkers_groups),
            placeholder ="Select a dataset"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Feature : "),
        dcc.Dropdown(
            id ='select_biomarkers_of_group',
            options = [{'value' : '', 'label' : ''}],
            placeholder = "Select a feature"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Filter with an Age range : "),
        dcc.RangeSlider(
            id='Age filter',
            min=35,
            max=85,
            value=[10, 100],
            marks = dict(zip(range(35, 85 + 1, 5), [str(elem) for elem in range(35, 85 + 1, 5)])),
            step=None
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Ethnicity : "),
        dcc.Dropdown(
            id='Ethnicity filter',
            options = get_dataset_options(ETHNICITY_COLS),
            placeholder = "Select an ethnicity"
            ),
        html.Br()
    ]),
])

table_df = pd.DataFrame(data = {'Sex' : ['All', 'Male', 'Female'], 'corr' : [0, 0, 0], 'coef' : [0, 0, 0], 'p_value': [0, 0, 0]})
table = dbc.Card([
    dbc.FormGroup([
        html.P("p_value, corr, coef results for all sexes : "),
        dash_table.DataTable(
            id = 'table',
            columns =[{"name": i, "id": i} for i in table_df.columns],
            data = table_df.to_dict('records')
        ),
        html.Br()
    ])
])


layout = dbc.Container([
                html.H1('Biomarkers'),
                html.Br(),
                html.Br(),
                dcc.Loading([
                    dbc.Row([
                        dbc.Col([controls,
                                 html.Br(),
                                 html.Br(),
                                 table], md=3),
                        dbc.Col(
                            [dcc.Graph(
                                 id='Plot Distribution feature'
                                 ),
                             dcc.Graph(
                                 id='Plot Reglin_all'
                                 ),
                             dcc.Graph(
                                 id='Plot Volcano'
                                 )],
                             md=9)
                            ])
                        ])
            ], fluid = True)


@app.callback(Output('select_biomarkers_of_group', 'options'),
              [Input('select_group_biomarkers', 'value')])
def generate_list_features_given_group_pf_biomarkers(value):
    if value is None:
        return [{'value' : '', 'label' : ''}]
    else :
        cols = pd.read_csv(path_inputs + '/' + value + '.csv', nrows = 10).set_index('id').columns
        cols = [ elem for elem in cols if elem not in ETHNICITY_COLS + ['Age when attended assessment centre', 'eid', 'Sex']]
        return get_dataset_options(cols)

# small test :
@app.callback([Output('Plot Distribution feature', 'figure'),Output('Plot Reglin_all', 'figure'), Output('table', 'data'), Output('Plot Volcano', 'figure')],
              [Input('select_group_biomarkers', 'value'), Input('select_biomarkers_of_group', 'value'), Input('Age filter', 'value'), Input('Ethnicity filter', 'value')])
def plot_distribution_of_feature(value_group, value_feature, value_age_filter, value_ethnicity):
    print(value_group, value_feature, value_age_filter)

    fig = {'layout' : dict(title='Distribution of the feature', # title of plot
                           xaxis={'title' : 'Value'}, # xaxis label
                           yaxis={'title' : 'Count'}, # yaxis label
                           bargap=0.2, # gap between bars of adjacent location coordinates
                           bargroupgap=0.1, # gap between bars of the same location coordinates))
                           legend=dict(orientation='h')
                           )}

    fig2 = {'layout' : dict(title='Feature = f(Age)', # title of plot
                            xaxis={'title' :'Age'}, # xaxis label
                            yaxis={'title' :'feature value'},
                            legend=dict(orientation='h')
                            )}

    fig3 = {'layout' : dict(title='Volcano plot', # title of plot
                            legend=dict(orientation='h'),
                            xaxis={'title' :'Pearson Correlation'}, # xaxis label
                            yaxis={'title' :'-log(p_value)'}
                            )}

    if value_group is not None :
        features_p_val = pd.read_csv(path_linear + 'linear_correlations_%s.csv' % value_group)
        features_p_val['p_val'] = features_p_val['p_val'].replace(0, 1e-323)
        print(features_p_val)
        hovertemplate = 'Feature : %{customdata[0]}\
                         <br>p_value : %{customdata[1]:.3E}\
                         <br>Correlation : %{customdata[2]:.3f}\
                         <br>Sample Size : %{customdata[3]}'
        customdata = np.stack([features_p_val['feature_name'], features_p_val['p_val'], features_p_val['corr_value'], features_p_val['size_na_dropped']], axis=-1)
        print(customdata)
        fig3['data'] = [go.Scatter(x = features_p_val['corr_value'],
                                   y = -np.log10(features_p_val['p_val']),
                                   mode='markers',
                                   showlegend = False,
                                   name = '',
                                   hovertemplate = hovertemplate,
                                   customdata=customdata)]
        num_tests = features_p_val.shape[0]
        shapes = []
        line = dict(
            color="Black",
            width=0.5
                  )
        fig3['data'].append(
            go.Scatter(x = [features_p_val['corr_value'].min() - features_p_val['corr_value'].std(), features_p_val['corr_value'].max() + features_p_val['corr_value'].std()],
                       y = [-np.log((5/100)), -np.log((5/100))],
                       name = 'No Correction',
                       mode = 'lines'))
        fig3['data'].append(
            go.Scatter(x = [features_p_val['corr_value'].min() - features_p_val['corr_value'].std(), features_p_val['corr_value'].max() + features_p_val['corr_value'].std()],
                       y = [-np.log((5/100)/num_tests), -np.log((5/100)/num_tests)],
                       name = 'With Bonferoni Correction',
                       mode = 'lines'))





    if value_group is not None and value_feature is not None:
        ## Load Data :
        df_bio = pd.read_csv(path_inputs + '/%s.csv' % value_group).set_index('id').dropna()
        df = df_sex_age_ethnicity_eid.join(df_bio, rsuffix = '_r').dropna()
        df = df[df.columns[~df.columns.str.contains('_r')]]
        df = df[(df['Age when attended assessment centre'] < value_age_filter[1]) & (df['Age when attended assessment centre'] > value_age_filter[0]) ]
        if value_ethnicity is not None:
            df = df[df[value_ethnicity] == 1]
        ## Generate histogram
        fig['layout']['title'] = ' %s ' % value_feature

        fig['data'] = [] # [go.Histogram(x = df[value_feature], name = value_feature, histnorm='percent')]

        ## Generate reglin all
        lin_age = LinearRegression()
        lin_age.fit(df[ETHNICITY_COLS + ['Sex']].values, df['Age when attended assessment centre'].values)
        res_age = df['Age when attended assessment centre'].values - lin_age.predict(df[ETHNICITY_COLS + ['Sex']].values)

        lin_feature = LinearRegression()
        lin_feature.fit(df[ETHNICITY_COLS + ['Sex']].values, df[value_feature].values)
        res_feature = df[value_feature].values - lin_feature.predict(df[ETHNICITY_COLS + ['Sex']].values)

        corr_all, p_val = pearsonr(res_age, res_feature)
        slope_all, intercept_all, r_value, p_val_all, std_err = linregress(df['Age when attended assessment centre'],df[value_feature])

        plot_points = go.Scattergl(x = df['Age when attended assessment centre'],
                                   y = df[value_feature],
                                   name = value_feature,
                                   opacity=0.3,
                                   marker=dict(
                                       color='Grey',
                                       size=2),
                                   mode='markers')
        lin_all = go.Scatter(x = df['Age when attended assessment centre'],
                             y = slope_all * df['Age when attended assessment centre'] + intercept_all,
                             name = 'All',
                             line=dict(color="Black"))

        ## Generate reglin male
        df_male = df[df.Sex == 1]
        lin_age = LinearRegression()
        lin_age.fit(df_male[ETHNICITY_COLS + ['Sex']].values, df_male['Age when attended assessment centre'].values)
        res_age = df_male['Age when attended assessment centre'].values - lin_age.predict(df_male[ETHNICITY_COLS + ['Sex']].values)

        lin_feature = LinearRegression()
        lin_feature.fit(df_male[ETHNICITY_COLS + ['Sex']].values, df_male[value_feature].values)
        res_feature = df_male[value_feature].values - lin_feature.predict(df_male[ETHNICITY_COLS + ['Sex']].values)

        corr_male, p_val = pearsonr(res_age, res_feature)
        slope_male, intercept_male, r_value, p_val_male, std_err = linregress(df_male['Age when attended assessment centre'],df_male[value_feature])
        lin_male = go.Scatter(x = df_male['Age when attended assessment centre'],
                              y = slope_male * df_male['Age when attended assessment centre'] + intercept_male,
                              name = 'Males',
                              line=dict(color="Blue"))
        fig['data'].append(go.Histogram(x = df_male[value_feature],
                                        name = 'Males',
                                        histnorm='percent',
                                        marker = dict(color = 'Blue')))
        ## Generate reglin female
        df_female = df[df.Sex == 0]
        lin_age = LinearRegression()
        lin_age.fit(df_female[ETHNICITY_COLS + ['Sex']].values, df_female['Age when attended assessment centre'].values)
        res_age = df_female['Age when attended assessment centre'].values - lin_age.predict(df_female[ETHNICITY_COLS + ['Sex']].values)

        lin_feature = LinearRegression()
        lin_feature.fit(df_female[ETHNICITY_COLS + ['Sex']].values, df_female[value_feature].values)
        res_feature = df_female[value_feature].values - lin_feature.predict(df_female[ETHNICITY_COLS + ['Sex']].values)

        corr_female, p_val = pearsonr(res_age, res_feature)
        slope_female, intercept_female, r_value, p_val_female, std_err = linregress(df_female['Age when attended assessment centre'],df_female[value_feature])
        lin_female = go.Scatter(x = df_female['Age when attended assessment centre'],
                                y = slope_female * df_female['Age when attended assessment centre'] + intercept_female,
                                name = 'Females',
                                line=dict(color="#ff93ac"))
        fig['data'].append(go.Histogram(x = df_female[value_feature],
                                        name = 'Females',
                                        histnorm='percent',
                                        marker=dict(color = '#ff93ac')))
        fig2 = {'data' : [lin_all, lin_male, lin_female, plot_points],
                'layout' : dict(title='%s = f(Age)' % value_feature,#, p_val=%.3f, corr=%.3f, slope=%.3f, Ethnicity=%s' % (p_val, corr, slope, value_ethnicity), # title of plot
                                xaxis={'title' : 'Age'}, # xaxis label
                                yaxis={'title' : value_feature},
                                legend=dict(orientation='h')
                                )}
        table_df_up = pd.DataFrame(data = {'Sex' : ['All', 'Male', 'Female'],
                                           'corr' : ['%.3f' % corr_all, '%.3f' % corr_male, '%.3f' % corr_female],
                                           'coef' : ['%.3f' % slope_all, '%.3f' % slope_male, '%.3f' % slope_female],
                                           'p_value': ['%.3E' % p_val_all, '%.3E' % p_val_male, '%.3E' % p_val_female]})
        table_df_up = table_df_up.to_dict('records')
        return fig, fig2, table_df_up, fig3
    else :
        return fig, fig2, table_df.to_dict('records'), fig3
