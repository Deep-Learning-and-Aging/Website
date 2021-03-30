from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_category_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_options,
    get_dimension_drop_down,
)
from dash_website.utils.aws_loader import load_csv, load_excel
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Select Category", tab_id="tab_category"),
                    dbc.Tab(label="Select Dimension", tab_id="tab_dimension"),
                    dbc.Tab(label="Select Average", tab_id="tab_average"),
                ],
                id="tab_manager",
                active_tab="tab_average",
            ),
            html.Div(id="tab_content"),
        ]
    )


@APP.callback(Output("tab_content", "children"), Input("tab_manager", "active_tab"))
def _fill_tab(active_tab):
    if active_tab == "tab_category":
        controls = get_controls_tab_category()
        title_id = "scores_category"
        graph_id = "graph_category"
    elif active_tab == "tab_dimension":
        controls = get_controls_tab_dimension()
        title_id = "scores_dimension"
        graph_id = "graph_dimension"
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


def get_controls_tab_category():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_category", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_category_drop_down("category_category"),
            get_subset_method_radio_items("subset_method_category"),
            get_correlation_type_radio_items("correlation_type_category"),
        ]
    )


@APP.callback(
    [Output("category_category", "options"), Output("category_category", "value")],
    Input("main_category_category", "value"),
)
def _change_category_category(main_category):
    return get_options(["All"] + MAIN_CATEGORIES_TO_CATEGORIES[main_category]), "All"


def get_controls_tab_dimension():
    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension", DIMENSIONS),
            get_subset_method_radio_items("subset_method_dimension"),
            get_correlation_type_radio_items("correlation_type_dimension"),
        ]
    )


def get_controls_tab_average():
    return dbc.Card(
        [
            get_dimension_drop_down(
                "dimension_1_average", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_dimension=1
            ),
            html.Div(
                [get_dimension_drop_down("dimension_2_average", ["Average"] + DIMENSIONS, idx_dimension=2)],
                id="hiden_dimension_2_average",
                style={"display": "block"},
            ),
            get_subset_method_radio_items("subset_method_average"),
            get_correlation_type_radio_items("correlation_type_average"),
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
