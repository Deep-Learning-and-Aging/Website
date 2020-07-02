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



path_performance = '/Users/samuel/Desktop/dash_app/data/for_Samuel/'
organs = ['Eyes','FullBody','Heart','Hips','Pancreas','Knees','Liver','Spine','Brain','Carotids']


controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select eid vs instances : "),
        dcc.RadioItems(
            id = 'select_eid_or_instances_res',
            options = get_dataset_options(['*', 'instances', 'eids']),
            value = '*',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select aggregate type : "),
        dcc.RadioItems(
            id ='select_aggregate_type_res',
            options = get_dataset_options(['bestmodels', 'All']),
            value = 'bestmodels',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_res',
            options = get_dataset_options(organs + ['All']),
            placeholder = 'All',
            value = 'All'
            ),
        html.Br()
    ], id = 'select_organ_res_full'),
    dbc.FormGroup([
        html.P("Select step : "),
        dcc.Dropdown(
            id='Select_step_res',
            options = get_dataset_options(['Test', 'Validation', 'Train']),
            value = 'Test'
            ),
        html.Br()
    ]),
])

layout = dbc.Container([
                html.H1('Correlations between accelerated aging'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [dcc.Loading([
                            dcc.Graph(
                             id='Plot Corr Heatmap'
                             ),
                         ])],
                        style={'overflowY': 'scroll', 'height': 1000, 'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                        ])
            ], fluid = True)


def LoadData(value_eid_vs_instances, value_aggregate, value_organ, value_step):
    dict_value_step_value = dict(zip(['Validation', 'Train', 'Test'], ['val', 'train', 'test']))
    if value_aggregate == 'bestmodels':
        df = pd.read_csv(path_performance + 'ResidualsCorrelations_bestmodels_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))
        std = pd.read_csv(path_performance + 'ResidualsCorrelations_bestmodels_sd_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))
        if value_eid_vs_instances == '*':
            df_instances = pd.read_csv(path_performance + 'ResidualsCorrelations_bestmodels_%s_Age_%s.csv' % ('*', dict_value_step_value[value_step]))
    else :
        df = pd.read_csv(path_performance + 'ResidualsCorrelations_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))
        std = pd.read_csv(path_performance + 'ResidualsCorrelations_sd_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))
        if value_eid_vs_instances == '*':
            df_instances = pd.read_csv(path_performance + 'ResidualsCorrelations_%s_Age_%s.csv' % ('*', dict_value_step_value[value_step]))

    index_std = std.columns[0]
    index = df.columns[0]
    std = std.set_index(index_std)
    df = df.set_index(index)
    std.index.name = 'Models'
    df.index.name = 'Models'

    df.index = ['-'.join(elem.split('_')[:4]) for elem in df.index.values]
    df.columns = ['-'.join(elem.split('_')[:4]) for elem in df.index.values]

    std.index = ['-'.join(elem.split('_')[:4]) for elem in std.index.values]
    std.columns = ['-'.join(elem.split('_')[:4]) for elem in std.index.values]
    if value_eid_vs_instances != '*':
        if value_aggregate == 'bestmodels':
            scores = pd.read_csv(path_performance + 'PERFORMANCES_bestmodels_ranked_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')
            scores.index = [elem.split('_')[1] for elem in scores.index.values]
            intersect = scores.index.intersection(df.index)
            customdata_score = scores.loc[intersect]
            df = df.loc[intersect, intersect]
            std = std.loc[intersect, intersect]
        else :
            scores = pd.read_csv(path_performance + 'PERFORMANCES_withEnsembles_ranked_%s_Age_%s.csv' % (value_eid_vs_instances, dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')
            scores.index = ['-'.join(elem.split('_')[1:5]) for elem in scores.index.values]
            customdata_score = scores.loc[df.index]
        customdata_score = customdata_score['R-Squared_all']
        customdata_score_x = np.tile(customdata_score, (len(customdata_score), 1))
        customdata_score_y = customdata_score_x.T


    else :
        if value_aggregate == 'bestmodels':
            scores_instances = pd.read_csv(path_performance + 'PERFORMANCES_bestmodels_ranked_instances_Age_%s.csv' % (dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')
            scores_eids = pd.read_csv(path_performance + 'PERFORMANCES_bestmodels_ranked_eids_Age_%s.csv' % (dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')
        else :
            scores_instances = pd.read_csv(path_performance + 'PERFORMANCES_withEnsembles_ranked_instances_Age_%s.csv' % (dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')
            scores_eids = pd.read_csv(path_performance + 'PERFORMANCES_withEnsembles_ranked_eids_Age_%s.csv' % (dict_value_step_value[value_step]))[['version', 'R-Squared_all']].set_index('version')

        index = df_instances.columns[0]
        df_instances = df_instances.set_index(index)
        df_instances.index.name = 'Models'
        df_instances.index = ['-'.join(elem.split('_')[:4]) for elem in df_instances.index.values]
        df_instances.columns = ['-'.join(elem.split('_')[:4]) for elem in df_instances.index.values]
        if value_aggregate == 'bestmodels':
            scores_instances.index = [elem.split('_')[1] for elem in scores_instances.index.values]
            scores_eids.index = [elem.split('_')[1] for elem in scores_eids.index.values]
            intersect = scores_instances.index.intersection(df.index)
            customdata_score_eids = scores_eids.loc[intersect]
            customdata_score_instances = scores_instances.loc[intersect]
            df = df.loc[intersect, intersect]
            std = std.loc[intersect, intersect]
            df_instances = df.loc[intersect, intersect]
        else :
            scores_instances.index = ['-'.join(elem.split('_')[1:5]) for elem in scores_instances.index.values]
            scores_eids.index = ['-'.join(elem.split('_')[1:5]) for elem in scores_eids.index.values]
            customdata_score_eids = scores_eids.loc[df.index.values]
            customdata_score_instances = scores_instances.loc[df.index.values]

        customdata_score_eids = customdata_score_eids['R-Squared_all'].values
        customdata_score_eids_x = np.tile(customdata_score_eids, (len(customdata_score_eids), 1))
        customdata_score_eids_y = customdata_score_eids_x.T

        customdata_score_instances = customdata_score_instances['R-Squared_all'].values
        customdata_score_instances_x = np.tile(customdata_score_instances, (len(customdata_score_instances), 1))
        customdata_score_instances_y = customdata_score_instances_x.T

        na_instances = df_instances.isna().values

        customdata_score_x = copy.deepcopy(df)
        customdata_score_y = copy.deepcopy(df)

        customdata_score_x.values[na_instances] = customdata_score_instances_x[na_instances]
        customdata_score_y.values[na_instances] = customdata_score_instances_y[na_instances]

        customdata_score_x.values[np.invert(na_instances)] = customdata_score_eids_x[np.invert(na_instances)]
        customdata_score_y.values[np.invert(na_instances)] = customdata_score_eids_y[np.invert(na_instances)]

    return customdata_score_x, customdata_score_y, df, std




@app.callback(Output('select_organ_res_full', 'style'),
              [Input('select_aggregate_type_res', 'value')])
def _hide_organ_dropdown(value_aggregate):
    if value_aggregate is not None and value_aggregate != 'All':
        return {'display': 'none'}
    else :
        return {}





@app.callback(Output('Plot Corr Heatmap', 'figure'),
              [Input('select_eid_or_instances_res', 'value'), Input('select_aggregate_type_res', 'value'), Input('Select_organ_res', 'value'), Input('Select_step_res', 'value')])
def _plot_r2_scores(value_eid_vs_instances, value_aggregate, value_organ, value_step):
    if value_aggregate is not None and value_organ is not None and value_step is not None:
        ## Load Data :
        customdata_score_x, customdata_score_y, df, std = LoadData(value_eid_vs_instances, value_aggregate, value_organ, value_step)
        print("customdata_score_x : ", customdata_score_x.shape)
        d = {}
        d['layout'] = dict(height = 1000,
                           width = 1000,
                           margin = {'l': 0, 'b': 110, 't': 0, 'r': 0},
                           xaxis = dict(titlefont=dict(size=8)),
                           yaxis = dict(titlefont=dict(size=8)),
                           plot_bgcolor='rgba(0,0,0,0)')
        ## Linear mapping
        def f(x):
            if x <= 0:
                return 'rgba(%s, %s, %s, 0.85)' % (255, 255*(x + 1), 255*(x + 1))
            else :
                return 'rgba(%s, %s, %s, 0.85)' % (255*(1 - x), 255*(1 - x), 255)

        if value_organ == 'All':
            min = df.min().min()
            max = df.max().max()
            abs = np.abs(min/(min - max))
            colorscale =  [[0, f(min)],
                           [abs, 'rgba(255, 255, 255, 0.85)'],
                           [1, f(max)]]
            if value_aggregate == 'All':
                ## REmove ticks labels :
                d['layout']['yaxis'] = dict(showticklabels=False)
                d['layout']['xaxis'] = dict(showticklabels=False)
                distincts_organs = list(set([elem.split('-')[0] for elem in df.index.values]))
                distincts_views = list(set([elem.split('-')[1] for elem in df.index.values]))
                list_elem_0 = np.char.array([elem.split('-') for elem in df.index])[:, 0]
                list_elem_1 = np.char.array([elem.split('-') for elem in df.index])[:, 1]
                list_elem_2 = np.char.array([elem.split('-') for elem in df.index])[:, 2]
                list_elem_3 = np.char.array([elem.split('-') for elem in df.index])[:, 3]

                x = df.index
                y = df.index

                ## Custom data & hovertemplate
                # 4 different values
                customdata_x = np.tile(list_elem_0, (len(list_elem_0), 1))
                customdata_y = customdata_x.T
                customdata_1_x = np.tile(list_elem_1, (len(list_elem_1), 1))
                customdata_1_y = customdata_1_x.T
                customdata_2_x = np.tile(list_elem_2, (len(list_elem_2), 1))
                customdata_2_y = customdata_2_x.T
                custom_data_3_x =  np.tile(list_elem_3, (len(list_elem_3), 1))
                custom_data_3_y =  custom_data_3_x.T
                # Std
                custom_data_std = std.values
                # Score
                customdata = np.dstack((customdata_x, customdata_y, customdata_1_x, customdata_1_y, customdata_2_x, customdata_2_y, custom_data_3_x, custom_data_3_y, custom_data_std, customdata_score_x, customdata_score_y))
                hovertemplate = 'Organ_x : %{customdata[0]}\
                                 <br>View x: %{customdata[2]}\
                                 <br>Transformation x : %{customdata[4]}\
                                 <br>Architecture x : %{customdata[6]}\
                                 <br>Score x : %{customdata[9]:.3f}\
                                 <br>\
                                 <br>Organ_y : %{customdata[1]}\
                                 <br>View y : %{customdata[3]}\
                                 <br>Transformation y : %{customdata[5]}\
                                 <br>Architecture y : %{customdata[7]}\
                                 <br>Score y : %{customdata[10]:.3f}\
                                 <br>\
                                 <br>Correlation : %{z:.3f} ± %{customdata[8]:.3f}'

                shapes = []
                annotations = []
                line = dict(
                    color="Black",
                    width=0.5
                          )
                for organ in distincts_organs:
                    x0 = -20.5
                    x1 = -40.5
                    where_organ = np.where(x.str.startswith(organ))[0]
                    min_organ = where_organ.min()
                    max_organ = where_organ.max()
                    shapes.append(dict(type="line",
                                       xref="x",
                                       yref="y",
                                       x0=x0,
                                       y0=min_organ - 0.5,
                                       x1=x1,
                                       y1=min_organ - 0.5,
                                       line = line
                                       )
                                  )
                    shapes.append(dict(type="line",
                                       xref="x",
                                       yref="y",
                                       x0=min_organ - 0.5,
                                       y0=x0,
                                       x1=min_organ - 0.5,
                                       y1=x1,
                                       line = line
                                       )
                                  )
                    annotations.append(dict(text = organ,
                                            xref="x",
                                            yref="y",
                                            x = (x0 + x1)/2,
                                            y = (max_organ + min_organ)/2,
                                            showarrow = False,
                                            font = dict(size = 7)
                                            )
                                       )
                    if organ in [',', '*', '?']:
                        textangle = 0
                    else :
                        textangle = -90
                    annotations.append(dict(text = organ,
                                            xref="x",
                                            yref="y",
                                            x = (max_organ + min_organ)/2,
                                            y = (x0 + x1)/2,
                                            showarrow = False,
                                            textangle=textangle,
                                            font = dict(size = 7)
                                            )
                                       )



                    distincts_views = x[x.str.startswith(organ)]
                    distincts_views = [elem.split('-')[1] for elem in distincts_views]
                    distincts_views = list(set(distincts_views))
                    x0 = -20.5
                    x1 = -0.5
                    for view in distincts_views:
                        where_organ_view = np.where(x.str.contains(organ + '-' + view, regex = False))[0]
                        min_view = where_organ_view.min()
                        max_view = where_organ_view.max()
                        ## Add bottom bar
                        shapes.append(dict(type="line",
                                           xref="x",
                                           yref="y",
                                           x0=x0,
                                           y0=min_view - 0.5,
                                           x1=x1,
                                           y1=min_view - 0.5,
                                           line = line
                                           )
                                      )
                        shapes.append(dict(type="line",
                                           xref="x",
                                           yref="y",
                                           x0=min_view - 0.5,
                                           y0=x0,
                                           x1=min_view - 0.5,
                                           y1=x1,
                                           line = line
                                           )
                                      )
                        ## Add annotation :
                        annotations.append(dict(text = view,
                                                xref="x",
                                                yref="y",
                                                x = (x0 + x1)/2,
                                                y = (max_view + min_view)/2,
                                                showarrow = False,
                                                font = dict(size = 7)
                                                )
                                           )
                        if view in [',', '*', '?']:
                            textangle = 0
                        else :
                            textangle = -90
                        annotations.append(dict(text = view ,
                                                xref="x",
                                                yref="y",
                                                x = (max_view + min_view)/2,
                                                y = (x0 + x1)/2,
                                                showarrow = False,
                                                textangle=textangle,
                                                font = dict(size = 7)
                                                )
                                           )
                ## Add final Bar
                shapes.append(dict(type="line",
                                   xref="x",
                                   yref="y",
                                   x0=-0.5,
                                   y0=len(x),
                                   x1=-40.5,
                                   y1=len(x),
                                   line = line
                                   )
                              )
                shapes.append(dict(type="line",
                                   xref="x",
                                   yref="y",
                                   x0=len(x),
                                   y0=-0.5,
                                   x1=len(x),
                                   y1=-40.5,
                                   line = line
                                   )
                              )
                colorbar = dict(len = 1000 - 250, lenmode = 'pixels', y = 0.58)
                d['layout']['shapes'] = shapes
                d['layout']['annotations'] = annotations

            else :
                x = df.index
                y = df.index


                hovertemplate = 'Organ_x : %{x}\
                                 <br>Score x : %{customdata[1]:.3f}\
                                 <br>\
                                 <br>Organ_y : %{y}\
                                 <br>Score y : %{customdata[2]:.3f}\
                                 <br>\
                                 <br>Correlation : %{z:.3f} ± %{customdata[0]:.3f}'
                print(std.values.shape, customdata_score_x)

                customdata = np.dstack([std.values, customdata_score_x, customdata_score_y])
                colorbar = None

            df_miror = 1*df.isna()
            df_miror = df_miror.replace(0, np.nan).values
            np.fill_diagonal(df_miror, 1)
            df = df.values
            np.fill_diagonal(df, np.nan)
            #print("x ", x.shape, "Total shape : ", df.shape, 'y ', y.shape)

            d['data'] = [
                        ## Actual plot
                        go.Heatmap(z=df,
                                    x=x,
                                    y=y,
                                    zsmooth=False,
                                    hoverongaps = False,
                                    colorscale=colorscale,
                                    customdata = customdata,
                                    hovertemplate = hovertemplate,
                                    colorbar = colorbar
                                    ),
                         ## Miror to fill na
                        go.Heatmap(z=df_miror,
                                   x=x,
                                   y=y,
                                   showlegend = False,
                                   showscale = False,
                                   hoverinfo='skip',
                                   colorscale = [[0, 'rgba(128,128,128, 0.7)'], [1, 'rgba(128,128,128, 0.7)']]
                                  )
                         ]


        else:
            mask = df.columns.str.contains(value_organ)
            customdata_score_x = customdata_score_x.iloc[mask, mask]
            customdata_score_y = customdata_score_y.iloc[mask, mask]

            df = df[df.columns[df.columns.str.contains(value_organ)]]
            df = df.loc[df.index.str.contains(value_organ)]
            std = std[std.columns[std.columns.str.contains(value_organ)]]
            std = std.loc[std.index.str.contains(value_organ)]
            if value_aggregate == 'All':
                list_elem_0 = np.char.array([elem.split('-') for elem in df.index])[:, 1]
                list_elem_1 = np.char.array([elem.split('-') for elem in df.index])[:, 2] + '_' + np.char.array([elem.split('-') for elem in df.index])[:, 3]
                x = [list_elem_0, list_elem_1]
                y = [list_elem_0, list_elem_1]
            else :
                x = df.index
                y = df.index

            list_elem_1 = np.char.array([elem.split('-') for elem in df.index])[:, 1]
            list_elem_2 = np.char.array([elem.split('-') for elem in df.index])[:, 2]
            list_elem_3 = np.char.array([elem.split('-') for elem in df.index])[:, 3]

            ## 3 Values
            customdata_1_x = np.tile(list_elem_1, (len(list_elem_1), 1))
            customdata_1_y = customdata_1_x.T
            customdata_2_x = np.tile(list_elem_2, (len(list_elem_2), 1))
            customdata_2_y = customdata_2_x.T
            custom_data_3_x =  np.tile(list_elem_3, (len(list_elem_3), 1))
            custom_data_3_y =  custom_data_3_x.T
            # Std
            custom_data_std = std.values
            # Score
            customdata = np.dstack((customdata_1_x, customdata_1_y, customdata_2_x, customdata_2_y, custom_data_3_x, custom_data_3_y, custom_data_std, customdata_score_x, customdata_score_y))
            hovertemplate = 'View x: %{customdata[0]}\
                             <br>Transformation x : %{customdata[2]}\
                             <br>Architecture x : %{customdata[4]}\
                             <br>Score x : %{customdata[7]:.3f}\
                             <br>\
                             <br>View y : %{customdata[1]}\
                             <br>Transformation y : %{customdata[3]}\
                             <br>Architecture y : %{customdata[5]}\
                             <br>Score x : %{customdata[8]:.3f}\
                             <br>\
                             <br>Correlation : %{z:.3f} ± %{customdata[6]:.3f}'
            min = df.min().min()
            max = df.max().max()
            abs = np.abs(min/(min - max))
            if abs > 0 and abs < 1 and min < 0 and max > 0:

                colorscale =  [[0, f(min)],
                               [abs, 'rgba(255, 255, 255, 0.85)'],
                               [1, f(max)]]
            else :
                colorscale = [[0, f(min)],
                               [1, f(max)]]


            df_miror = 1*df.isna()
            df_miror = df_miror.replace(0, np.nan).values
            np.fill_diagonal(df_miror, 1)
            df = df.values
            np.fill_diagonal(df, np.nan)

            d['data'] = [
                go.Heatmap(z=df,
                           x=x,
                           y=y,
                           colorscale=colorscale,
                           customdata=customdata,
                           hovertemplate=hovertemplate),
                go.Heatmap(z=df_miror,
                           x=x,
                           y=y,
                           showlegend = False,
                           showscale = False,
                           hoverinfo='skip',
                           colorscale = [[0, 'rgba(128,128,128, 0.7)'], [1, 'rgba(128,128,128, 0.7)']]
                           )
                ]

        return go.Figure(d)
    else :
        return go.Figure()
