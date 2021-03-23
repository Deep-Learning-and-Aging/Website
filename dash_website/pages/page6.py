from dash_website.app import app
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import numpy as np
import pandas as pd
from .tools import get_dataset_options, get_colorscale, empty_graph, load_csv
from plotly.graph_objs import Figure, Bar, Heatmap
import plotly.figure_factory as ff

from dash_website.pages.page17 import create_dfs
from dash_website.pages.page4 import LoadData
from dash_website.pages.utils.controls import (
    get_correlation_type_radio_items,
    get_subset_method_radio_items,
    get_organ_drop_down,
    get_category_radio_items,
    get_dataset_drop_down,
)
from dash_website.pages import (
    ORGANS,
    ALL_BIOMARKERS,
    ALL_ENVIRONMENTAL,
    ALL_SOCIOECONOMICS,
    ALL_PHENOTYPES,
    ALL_DISEASES,
    ALL,
    CATEGORIES,
)

path_correlations_ewas = "page6_LinearXWASCorrelations/CorrelationsLinear/"
colorscale = [[0, "rgba(255, 0, 0, 0.85)"], [0.5, "rgba(255, 255, 255, 0.85)"], [1, "rgba(0, 0, 255, 0.85)"]]


layout = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Select X", tab_id="tab_x"),
                dbc.Tab(label="Select Organ", tab_id="tab_organ"),
                dbc.Tab(label="Select Average", tab_id="tab_average"),
            ],
            id="tab_manager",
            active_tab="tab_x",
        ),
        html.Div(id="tab-content"),
    ]
)


@app.callback(Output("tab-content", "children"), Input("tab_manager", "active_tab"))
def _get_tab(active_tab):
    if active_tab == "tab_x":
        controls = get_controls_tab_x()
        title_id = "scores_x"
        graph_id = "graph_x"
    elif active_tab == "tab_organ":
        controls = get_controls_tab_organ()
        title_id = "scores_organ"
        graph_id = "graph_organ"
    else:  # active_tab == "tab_average"
        controls = get_controls_tab_average()
        title_id = "scores_average"
        graph_id = "graph_average"

    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([controls, html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id=title_id),
                                    dcc.Graph(id=graph_id),
                                ]
                            )
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab_x():
    return dbc.Card(
        [
            get_category_radio_items("category_x", CATEGORIES),
            get_correlation_type_radio_items("correlation_type_x"),
            get_subset_method_radio_items("subset_method_x"),
            get_dataset_drop_down("dataset_x"),
        ]
    )


def get_controls_tab_organ():
    return dbc.Card(
        [
            get_correlation_type_radio_items("correlation_type_organ"),
            get_subset_method_radio_items("subset_method_organ"),
            get_organ_drop_down("organs_organ", ORGANS),
        ]
    )


def get_controls_tab_average():
    return dbc.Card(
        [
            get_correlation_type_radio_items("correlation_type_average"),
            get_subset_method_radio_items("subset_method_average"),
        ]
    )


CATEGORIES = ["All", "Biomarkers", "Phenotypes", "Diseases", "Environmental", "Socioeconomics"]


@app.callback(Output("dataset_x", "options"), Input("category_x", "value"))
def _select_dataset(val_data_type):
    if val_data_type == "All":
        return [{"value": "All", "label": "All"}] + get_dataset_options(ALL)
    elif val_data_type == "Biomarkers":
        return [{"value": "All_Biomarkers", "label": "All_Biomarkers"}] + get_dataset_options(ALL_BIOMARKERS)
    elif val_data_type == "Phenotypes":
        return [{"value": "All_Phenotypes", "label": "All_Phenotypes"}] + get_dataset_options(ALL_PHENOTYPES)
    elif val_data_type == "Diseases":
        return [{"value": "All_Diseases", "label": "All_Diseases"}] + get_dataset_options(ALL_DISEASES)
    elif val_data_type == "Environmental":
        return [{"value": "All_Environmental", "label": "All_Environmental"}] + get_dataset_options(ALL_ENVIRONMENTAL)
    else:  # val_data_type == "Socioeconomics":
        return [{"value": "All_Socioeconomics", "label": "All_Socioeconomics"}] + get_dataset_options(
            ALL_SOCIOECONOMICS
        )


@app.callback(
    [Output("graph_average", "figure"), Output("scores_average", "children")],
    [Input("correlation_type_average", "value"), Input("subset_method_average", "value")],
)
def _plot_with_average_correlation(corr_type, subset_method):
    data = load_csv(path_correlations_ewas + "Correlations_%s_%s.csv" % (subset_method, corr_type)).replace("\\*", "*")
    correlation_data = pd.DataFrame(
        None,
        index=ALL
        + [
            "All",
            "All_Biomarkers",
            "All_Environmental",
            "All_Socioeconomics",
            "All_Phenotypes",
            "All_Diseases",
            "Genetics",
            "Phenotypic",
        ],
        columns=["mean", "std"],
    )

    genetics = create_dfs()[0]
    correlation_data.loc["Genetics", "mean"] = np.round_(np.nanmean(genetics.values), 3)
    correlation_data.loc["Genetics", "std"] = np.round_(np.nanstd(genetics.values), 3)

    phenotypic = LoadData("*", "bestmodels", None, "Test")[2]
    correlation_data.loc["Phenotypic", "mean"] = np.round_(np.nanmean(phenotypic.values), 3)
    correlation_data.loc["Phenotypic", "std"] = np.round_(np.nanstd(phenotypic.values), 3)

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


@app.callback(
    [Output("graph_organ", "figure"), Output("scores_organ", "children")],
    [
        Input("correlation_type_organ", "value"),
        Input("subset_method_organ", "value"),
        Input("organs_organ", "value"),
    ],
)
def _plot_with_given_organ_dataset(corr_type, subset_method, organ):
    if corr_type is not None and subset_method is not None:
        df = load_csv(path_correlations_ewas + "Correlations_%s_%s.csv" % (subset_method, corr_type)).replace(
            "\\*", "*"
        )
        df = df[["env_dataset", "organ_1", "organ_2", "corr", "sample_size"]]
        df_organ = df[df.organ_1 == organ]
        df_organ = df_organ[df_organ.organ_2 != organ]
        df_organ = df_organ.fillna(0)

        matrix_organ = pd.pivot_table(df_organ, values="corr", index=["env_dataset"], columns=["organ_2"])

        try:
            colorscale = get_colorscale(matrix_organ)
        except ValueError:
            return Figure(empty_graph)
        d = {}
        sample_size_matrix = pd.pivot_table(
            df_organ, values="sample_size", index=["env_dataset"], columns=["organ_2"]
        ).values
        customdata = np.dstack((sample_size_matrix, matrix_organ))
        title = "Average correlation = %.3f ± %.3f" % (
            np.mean(matrix_organ.values.flatten()),
            np.std(matrix_organ.values.flatten()),
        )
        hovertemplate = "Correlation : %{z}\
                 <br>Organ x : %{x}\
                 <br>Organ y : %{y}\
                 <br>Sample Size : %{customdata[0]}"

        d["data"] = Heatmap(
            z=matrix_organ.T,
            x=matrix_organ.T.columns,
            y=matrix_organ.T.index,
            colorscale=colorscale,
            customdata=customdata,
            hovertemplate=hovertemplate,
        )

        d["layout"] = dict(xaxis=dict(dtick=1), yaxis=dict(dtick=1), width=1000, height=600)
        return Figure(d), title
    else:
        return Figure(), ""


@app.callback(
    [Output("graph_x", "figure"), Output("scores_x", "children")],
    [
        Input("correlation_type_x", "value"),
        Input("subset_method_x", "value"),
        Input("dataset_x", "value"),
    ],
)
def _plot_with_given_organ_dataset(corr_type, subset_method, env_dataset):
    if corr_type is not None and subset_method is not None and env_dataset is not None:
        df = load_csv(path_correlations_ewas + "Correlations_%s_%s.csv" % (subset_method, corr_type)).replace(
            "\\*", "*"
        )
        df = df[["env_dataset", "organ_1", "organ_2", "corr", "sample_size"]]
        df_env = df[df.env_dataset == env_dataset]
        df_env = df_env.fillna(0)

        sample_size_matrix = pd.pivot_table(df_env, values="sample_size", index=["organ_1"], columns=["organ_2"])

        env_matrix = pd.pivot_table(df_env, values="corr", index=["organ_1"], columns=["organ_2"])
        labels = env_matrix.columns

        fig = ff.create_dendrogram(env_matrix, orientation="bottom", distfun=lambda df: 1 - df)
        for scatter in fig["data"]:
            scatter["yaxis"] = "y2"

        order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))

        fig.update_layout(xaxis={"ticktext": labels[order_dendrogram], "mirror": False})
        fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})

        heat_data = env_matrix.values[order_dendrogram, :]
        heat_data = heat_data[:, order_dendrogram]
        try:
            colorscale = get_colorscale(heat_data)
        except ValueError:
            return Figure(empty_graph)

        heat_sample_size = sample_size_matrix.values[order_dendrogram, :]
        heat_sample_size = heat_sample_size[:, order_dendrogram]
        customdata = np.dstack((heat_sample_size, heat_data))
        hovertemplate = "Correlation : %{z}\
                            <br>Organ x : %{x}\
                            <br>Organ y : %{y}\
                            <br>Sample Size : %{customdata[0]}"
        idx_upper = np.triu_indices(len(heat_data))
        title = "Average correlation = %.3f ± %.3f" % (np.mean(heat_data), np.std(heat_data))

        heatmap = Heatmap(
            x=labels[order_dendrogram],
            y=labels[order_dendrogram],
            z=heat_data,
            colorscale=colorscale,
            customdata=customdata,
            hovertemplate=hovertemplate,
        )

        heatmap["x"] = fig["layout"]["xaxis"]["tickvals"]
        heatmap["y"] = fig["layout"]["xaxis"]["tickvals"]

        fig.update_layout(
            yaxis={
                "domain": [0, 0.85],
                "mirror": False,
                "showgrid": False,
                "zeroline": False,
                "ticktext": labels[order_dendrogram],
                "tickvals": fig["layout"]["xaxis"]["tickvals"],
                "showticklabels": True,
                "ticks": "outside",
            }
        )

        fig.add_trace(heatmap)

        fig["layout"]["width"] = 1100
        fig["layout"]["height"] = 1100

        return fig, title  # Figure(d), title
    else:
        return Figure(), ""
