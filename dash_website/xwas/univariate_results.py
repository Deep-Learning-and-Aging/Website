import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_website.pages.tools import ETHNICITY_COLS, empty_graph, load_csv
from pandas import concat, Index, DataFrame
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar, Heatmap
from botocore.exceptions import ClientError
from dash_website.app import APP, MODE
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy

import pandas as pd

from dash_website.utils.controls import (
    get_dataset_options,
    get_dimension_drop_down,
    get_main_category_radio_items,
    get_category_drop_down,
)
from dash_website.utils.aws_loader import load_csv, load_excel, load_feather
from dash_website import (
    DIMENSIONS,
    ALL_BIOMARKERS,
    ALL_PHENOTYPES,
    ALL_DISEASES,
    ALL_ENVIRONMENTAL,
    ALL_SOCIOECONOMICS,
    ALL_CATEGORIES,
    CATEGORIES,
)

path_linear_ewas = "page5_LinearXWASResults/LinearOutput/"


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Volcano", tab_id="tab_volcano"),
                    dbc.Tab(label="Summary", tab_id="tab_summary"),
                ],
                id="tab_manager",
                active_tab="tab_volcano",
            ),
            html.Div(id="tab_content"),
        ]
    )


@APP.callback(Output("tab_content", "children"), Input("tab_manager", "active_tab"))
def _get_tab(active_tab):
    if active_tab == "tab_volcano":
        controls = get_controls_tab_volcano()
    else:  # active_tab == "tab_summary"
        controls = get_controls_tab_summary()

    return dbc.Container(
        [
            html.H1("Univariate XWAS - Results"),
            html.Br(),
            html.Br(),
            dcc.Store(id="memory_volcano"),
            dbc.Row(
                [
                    dbc.Col([controls, html.Br(), html.Br()], md=3),
                    dbc.Col([dcc.Graph(id="graph_volcano")], md=9),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id="table_volcano",
                                columns=[
                                    {"name": i, "id": i}
                                    for i in [
                                        "Environmental Feature",
                                        "Organ",
                                        "X Dataset",
                                        "p_value",
                                        "Partial correlation",
                                        "Sample Size",
                                    ]
                                ],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ],
                        # style={'overflowY': 'scroll', 'height': 2000},
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab_volcano():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_volcano", CATEGORIES),
            get_category_drop_down("category_volcano"),
            get_dimension_drop_down("dimension_volcano", DIMENSIONS),
        ]
    )


@APP.callback(Output("category_volcano", "options"), Input("main_category_volcano", "value"))
def _change_controls_category(val_data_type):
    if val_data_type == "All":
        return get_dataset_options(["All"] + ALL_CATEGORIES)
    elif val_data_type == "Biomarkers":
        return get_dataset_options(["All_Biomarkers"] + ALL_BIOMARKERS)
    elif val_data_type == "Phenotypes":
        return get_dataset_options(["All_Phenotypes"] + ALL_PHENOTYPES)
    elif val_data_type == "Diseases":
        return get_dataset_options(["All_Diseases"] + ALL_DISEASES)
    elif val_data_type == "Environmental":
        return get_dataset_options(["All_Environmental"] + ALL_ENVIRONMENTAL)
    else:  # val_data_type == "Socioeconomics":
        return get_dataset_options(["All_Socioeconomics"] + ALL_SOCIOECONOMICS)


def get_controls_tab_summary():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_summary", CATEGORIES),
        ]
    )


@APP.callback(Output("memory_volcano", "data"), Input("dimension_volcano", "value"))
def _modify_store(dimension):
    return load_feather(f"xwas/univariate_results/linear_correlations_{dimension}.feather")


@APP.callback(
    Output("graph_volcano", "figure"),
    [Input("main_category_volcano", "value"), Input("category_volcano", "value"), Input("dimension_volcano", "value")],
)
def _fill_volcano_and_table(value_organ, value_data, value_datasets):
    fig = {
        "layout": dict(
            title="Volcano plot", xaxis_title="Partial correlation", yaxis_title="-log(p_value)"  # title of plot
        )
    }
    data = None
    if value_organ is not None and value_data is not None:
        list_df = []
        for idx, env_dataset in enumerate(globals()[value_data]):
            try:
                if value_organ == "*":
                    value_organ = "\\*"
                t = load_csv(path_linear_ewas + "linear_correlations_%s_%s.csv" % (env_dataset, value_organ))
                t["Env_Dataset"] = env_dataset
                list_df.append(t)
                if value_organ == "\\*":
                    value_organ = "*"
            except (FileNotFoundError, ClientError):
                continue

        if len(list_df) == 0:
            return Figure(empty_graph), {}
        res = concat(list_df)
        res["p_val"] = res["p_val"].replace(0, 1e-323)
        res["env_feature_name"] = res["env_feature_name"].str.replace(".0", "")

        # Remove rows with "sample size" < 10:
        res.drop(index=res[res["size_na_dropped"] < 10].index, inplace=True)

        if value_datasets != "All" or value_datasets is None:
            res = res[res.Env_Dataset.isin(value_datasets)]

        hovertemplate = "Feature : %{customdata[0]}\
                         <br>Organ : %{customdata[1]}\
                         <br>X Dataset : %{customdata[2]}\
                         <br>p_value : %{customdata[3]:.3E}\
                         <br>Partial correlation : %{customdata[4]:.3f}\
                         <br>Sample Size : %{customdata[5]}"

        fig["data"] = []
        for env_dataset in res.Env_Dataset.drop_duplicates():
            res_ = res[res.Env_Dataset == env_dataset]
            customdata = np.stack(
                [
                    res_["env_feature_name"],
                    res_["target_dataset_name"],
                    res_["Env_Dataset"],
                    res_["p_val"],
                    res_["corr_value"],
                    res_["size_na_dropped"],
                ],
                axis=-1,
            )
            fig["data"].append(
                Scatter(
                    x=res_["corr_value"],
                    y=-np.log10(res_["p_val"]),
                    mode="markers",
                    name=env_dataset,
                    hovertemplate=hovertemplate,
                    customdata=customdata,
                )
            )
        num_tests = res.shape[0]
        shapes = []
        line = dict(color="Black", width=0.5)
        fig["data"].append(
            Scatter(
                x=[
                    res["corr_value"].min() - res["corr_value"].std(),
                    res["corr_value"].max() + res["corr_value"].std(),
                ],
                y=[-np.log10((5 / 100)), -np.log10((5 / 100))],
                name="No Correction",
                mode="lines",
            )
        )
        fig["data"].append(
            Scatter(
                x=[
                    res["corr_value"].min() - res["corr_value"].std(),
                    res["corr_value"].max() + res["corr_value"].std(),
                ],
                y=[-np.log10((5 / 100) / num_tests), -np.log10((5 / 100) / num_tests)],
                name="With Bonferoni Correction",
                mode="lines",
            )
        )

        data = res.rename(
            columns=dict(
                zip(
                    [
                        "env_feature_name",
                        "target_dataset_name",
                        "Env_Dataset",
                        "p_val",
                        "corr_value",
                        "size_na_dropped",
                    ],
                    ["Environmental Feature", "Organ", "X Dataset", "p_value", "Partial correlation", "Sample Size"],
                )
            )
        ).to_dict("records")
    return Figure(fig), data


@APP.callback(
    Output("table_volcano", "data"),
    [Input("table_volcano", "sort_by"), Input("memory_volcano", "data"), Input("graph_volcano", "restyleData")],
)
def _sort_table(sort_by_col, data, restyle):
    df = DataFrame(data=data)
    df = df.reset_index()
    if sort_by_col is not None and len(sort_by_col):
        sorting = sort_by_col[0]
        ascending = sorting["direction"] == "asc"
        df = df.sort_values(sorting["column_id"], ascending=ascending)
    df = df.round(5)
    return df.to_dict("records")
