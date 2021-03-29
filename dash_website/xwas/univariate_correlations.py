from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_dataset_options,
    get_correlation_type_radio_items,
    get_subset_method_radio_items,
    get_organ_drop_down,
    get_category_radio_items,
    get_dataset_drop_down,
)
from dash_website.utils.aws_loader import load_csv, load_excel
from dash_website import (
    DIMENSIONS,
    ALL_BIOMARKERS,
    ALL_ENVIRONMENTAL,
    ALL_SOCIOECONOMICS,
    ALL_PHENOTYPES,
    ALL_DISEASES,
    ALL_CATEGORIES,
    CATEGORIES,
)


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Select X", tab_id="tab_x"),
                    dbc.Tab(label="Select Organ", tab_id="tab_organ"),
                    dbc.Tab(label="Select Average", tab_id="tab_average"),
                ],
                id="tab_manager",
                active_tab="tab_average",
            ),
            html.Div(id="tab_content"),
        ]
    )


@APP.callback(Output("tab_content", "children"), Input("tab_manager", "active_tab"))
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


@APP.callback(Output("dataset_x", "options"), Input("category_x", "value"))
def _change_controls_x(val_data_type):
    if val_data_type == "All":
        return [{"value": "All", "label": "All"}] + get_dataset_options(ALL_CATEGORIES)
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


def get_controls_tab_organ():
    return dbc.Card(
        [
            get_correlation_type_radio_items("correlation_type_organ"),
            get_subset_method_radio_items("subset_method_organ"),
            get_organ_drop_down("organs_organ", DIMENSIONS),
        ]
    )


def get_controls_tab_average():
    return dbc.Card(
        [
            get_correlation_type_radio_items("correlation_type_average"),
            get_subset_method_radio_items("subset_method_average"),
            get_organ_drop_down("organs_organ_1", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_organ=1),
            html.Div(
                [get_organ_drop_down("organs_organ_2", ["Average"] + DIMENSIONS, idx_organ=2)],
                id="hiden_organ_2",
                style={"display": "block"},
            ),
        ]
    )


@APP.callback(
    [
        Output("hiden_organ_2", component_property="style"),
        Output("organs_organ_2", "options"),
        Output("organs_organ_2", "value"),
    ],
    [
        Input("correlation_type_average", "value"),
        Input("subset_method_average", "value"),
        Input("organs_organ_1", "value"),
        Input("organs_organ_2", "value"),
    ],
)
def _change_controls_average(correlation_type, subset_method, organ_1, organ_2):
    if organ_1 in ["MainDimensions", "SubDimensions"]:
        return {"display": "none"}, get_dataset_options(["Average"]), "Average"
    else:
        options_organ_2 = (
            load_excel(
                f"page6_LinearXWASCorrelations/average_correlations/Correlations_comparisons_{subset_method}_{correlation_type}.xlsx",
                index_col=[0, 1],
            )
            .loc[organ_1]
            .index
        )
        return {"display": "block"}, get_dataset_options(options_organ_2), organ_2


@APP.callback(
    [Output("graph_x", "figure"), Output("scores_x", "children")],
    [
        Input("correlation_type_x", "value"),
        Input("subset_method_x", "value"),
        Input("dataset_x", "value"),
    ],
)
def _fill_graph_tab_x(correlation_type, subset_method, dataset_x):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap

    correlations_raw = load_csv(
        f"page6_LinearXWASCorrelations/correlations/Correlations_{subset_method}_{correlation_type}.csv",
        usecols=["env_dataset", "organ_1", "organ_2", "corr", "sample_size"],
    ).replace("\\*", "*")

    correlations = correlations_raw[correlations_raw.env_dataset == dataset_x].fillna(0)
    sample_sizes_2d = pd.pivot_table(correlations, values="sample_size", index=["organ_1"], columns=["organ_2"])
    correlations_2d = pd.pivot_table(correlations, values="corr", index=["organ_1"], columns=["organ_2"])

    fig = create_dendrogram_heatmap(correlations_2d, sample_sizes_2d)

    title = "Average correlation = ??? ± ???"

    return fig, title


@APP.callback(
    [Output("graph_organ", "figure"), Output("scores_organ", "children")],
    [
        Input("correlation_type_organ", "value"),
        Input("subset_method_organ", "value"),
        Input("organs_organ", "value"),
    ],
)
def _fill_graph_tab_organ(correlation_type, subset_method, organ):
    from plotly.graph_objs import Figure
    from dash_website.utils.graphs.heatmap import create_heatmap

    correlations_raw = load_csv(
        f"page6_LinearXWASCorrelations/correlations/Correlations_{subset_method}_{correlation_type}.csv",
        usecols=["env_dataset", "organ_1", "organ_2", "corr", "sample_size"],
    ).replace("\\*", "*")
    correlations = correlations_raw[(correlations_raw.organ_1 == organ) & (correlations_raw.organ_2 != organ)].fillna(0)

    correlations_2d = pd.pivot_table(correlations, values="corr", index=["organ_2"], columns=["env_dataset"])
    sample_sizes_2d = pd.pivot_table(correlations, values="sample_size", index=["organ_2"], columns=["env_dataset"])

    heatmap = create_heatmap(correlations_2d, sample_sizes_2d, correlations_2d.columns, correlations_2d.index)
    title = "Average correlation = ??? ± ???"

    return Figure(heatmap), title


@APP.callback(
    [Output("graph_average", "figure"), Output("scores_average", "children")],
    [
        Input("correlation_type_average", "value"),
        Input("subset_method_average", "value"),
        Input("organs_organ_1", "value"),
        Input("organs_organ_2", "value"),
    ],
)
def _fill_graph_tab_average(correlation_type, subset_method, organ_1, organ_2):
    from plotly.graph_objs import Figure
    from dash_website.utils.graphs.bar import create_bar

    correlations_mean = load_excel(
        f"page6_LinearXWASCorrelations/average_correlations/Correlations_comparisons_{subset_method}_{correlation_type}.xlsx",
        index_col=[0, 1],
    ).loc[(organ_1, organ_2)]
    correlations_std = load_excel(
        f"page6_LinearXWASCorrelations/average_correlations/Correlations_sd_comparisons_{subset_method}_{correlation_type}.xlsx",
        index_col=[0, 1],
    ).loc[(organ_1, organ_2)]

    fig = Figure()
    fig.add_trace(create_bar(correlations_mean, correlations_std))
    fig.update_layout(xaxis_tickangle=-90)
    fig.update_layout({"width": 1800, "height": 600})

    return fig, f"{organ_1}_{organ_2}"
