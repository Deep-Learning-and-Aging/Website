from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options
from dash_website import (
    DOWNLOAD_CONFIG,
    MAIN_CATEGORIES_TO_CATEGORIES,
    DIMENSIONS,
    ALGORITHMS_RENDERING,
    CORRELATION_TYPES,
)
from dash_website.xwas import BAR_PLOT_TABLE_COLUMNS, FEATURES_CORRELATIONS_TABLE_COLUMNS


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_features"), dcc.Store(id="memory_scores", data=get_data())]),
            html.H1("Multivariate XWAS - Feature importances"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_features(), html.Br(), html.Br(), get_controls_table_features()], md=5),
                    dbc.Col(
                        dcc.Loading(
                            [
                                html.H2(id="title_feature_importances"),
                                dcc.Graph(id="bar_plot_features", config=DOWNLOAD_CONFIG),
                            ]
                        ),
                        md=7,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id="table_features",
                                columns=[{"name": i, "id": i} for i in list(BAR_PLOT_TABLE_COLUMNS.values())],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ],
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather(
        f"xwas/multivariate_results/scores.feather", columns=["category", "dimension", "r2", "std", "algorithm"]
    ).to_dict()


@APP.callback(
    Output("memory_features", "data"), [Input("dimension_features", "value"), Input("category_features", "value")]
)
def _modify_store_features(dimension, category):
    return load_feather(
        f"xwas/multivariate_feature_importances/dimension_category/features_{dimension}_{category}.feather"
    ).to_dict()


def get_controls_features():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_features",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_features", ["..."], "Select X subcategory: ", from_dict=False),
            get_drop_down(
                "dimension_features",
                DIMENSIONS,
                "Select an aging dimension: ",
                from_dict=False,
            ),
        ]
    )


@APP.callback(
    [Output("category_features", "options"), Output("category_features", "value")],
    Input("main_category_features", "value"),
)
def _change_controls_category(main_category):
    if main_category == "All":
        list_categories = list(
            pd.Index(MAIN_CATEGORIES_TO_CATEGORIES[main_category]).drop(["Genetics", "Phenotypic", "PhysicalActivity"])
        )
    elif main_category == "Biomarkers":
        list_categories = list(pd.Index(MAIN_CATEGORIES_TO_CATEGORIES[main_category]).drop(["PhysicalActivity"]))
    else:
        list_categories = MAIN_CATEGORIES_TO_CATEGORIES[main_category]
    return get_options(list_categories), list_categories[0]


def get_controls_table_features():
    return dbc.Card(
        [
            get_item_radio_items("correlation_type_features", CORRELATION_TYPES, "Select correlation type :"),
            dbc.FormGroup(
                [
                    html.P("Correlation between feature importances/correlation : "),
                    dash_table.DataTable(
                        id="table_correlation_features",
                        columns=[{"name": i, "id": i} for i in list(FEATURES_CORRELATIONS_TABLE_COLUMNS.values())],
                        style_cell={"textAlign": "left"},
                        sort_action="custom",
                        sort_mode="single",
                    ),
                    html.Br(),
                ]
            ),
        ]
    )


@APP.callback(
    [
        Output("bar_plot_features", "figure"),
        Output("table_features", "data"),
        Output("table_correlation_features", "data"),
        Output("title_feature_importances", "children"),
    ],
    [
        Input("dimension_features", "value"),
        Input("category_features", "value"),
        Input("correlation_type_features", "value"),
        Input("memory_features", "data"),
        Input("memory_scores", "data"),
    ],
)
def _fill_bar_plot_feature(dimension, category, correlation_type, data_features, data_scores):
    import plotly.graph_objects as go

    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "category"])
    if (dimension, category) in scores_raw.index:
        scores = scores_raw.loc[dimension, category]
        best_algorithm = scores.iloc[scores["r2"].argmax()]["algorithm"]

        scores_algorithm = scores.reset_index().set_index("algorithm").round(3)
        title = f"R² : Elastic Net {scores_algorithm.loc['elastic_net', 'r2']} +- {scores_algorithm.loc['elastic_net', 'std']}, "
        title += f"Light GBM {scores_algorithm.loc['light_gbm', 'r2']} +- {scores_algorithm.loc['light_gbm', 'std']}, Neural Network {scores_algorithm.loc['neural_network', 'r2']} +- {scores_algorithm.loc['neural_network', 'std']}"
    else:
        scores = None
        best_algorithm = "light_gbm"
        title = "We don't have the scores for the moment, they are going to be uploaded soon."

    features = pd.DataFrame(data_features).set_index(["algorithm", "variable"])
    sorted_variables = (
        (features.loc[best_algorithm].abs() / features.loc[best_algorithm].abs().sum())
        .sort_values(by=["feature_importance"], ascending=False)
        .index
    )

    algorithms = features.index.get_level_values("algorithm").drop_duplicates()

    table_features = pd.DataFrame(None, columns=BAR_PLOT_TABLE_COLUMNS.keys())
    table_features["variable"] = sorted_variables

    for algorithm in algorithms:
        sorted_algorithm_variable = [[algorithm, variable] for variable in sorted_variables]

        table_features[f"feature_{algorithm}"] = features.loc[sorted_algorithm_variable].values
        table_features[f"percentage_{algorithm}"] = (
            features.loc[sorted_algorithm_variable].abs() / features.loc[sorted_algorithm_variable].abs().sum()
        )["feature_importance"].values

    bars = []
    hovertemplate = "Variable: %{y} <br>Percentage of overall feature importance: %{x:.3f} <br>Feature importance: %{customdata:.3f} <br><extra></extra>"

    for algorithm in algorithms:
        bars.append(
            go.Bar(
                name=ALGORITHMS_RENDERING[algorithm],
                x=table_features[f"percentage_{algorithm}"].values[::-1],
                y=sorted_variables[::-1],
                orientation="h",
                customdata=table_features[f"feature_{algorithm}"].values[::-1],
                hovertemplate=hovertemplate,
            )
        )

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 800,
            "height": int(25 * len(sorted_variables)),
            "xaxis": {"title": "Percentage of overall feature importance", "showgrid": False},
            "yaxis": {"title": "Variables", "showgrid": False},
        }
    )

    table_correlations_raw = table_features[
        [
            f"percentage_{'correlation'}",
            f"percentage_{'elastic_net'}",
            f"percentage_{'light_gbm'}",
            f"percentage_{'neural_network'}",
        ]
    ]

    table_correlations = (
        table_correlations_raw.corr(method=correlation_type)
        .round(3)
        .rename(index=FEATURES_CORRELATIONS_TABLE_COLUMNS)
        .reset_index()
    )

    return (
        fig,
        table_features.round(3).rename(columns=BAR_PLOT_TABLE_COLUMNS).to_dict("records"),
        table_correlations.rename(columns=FEATURES_CORRELATIONS_TABLE_COLUMNS).to_dict("records"),
        title,
    )
