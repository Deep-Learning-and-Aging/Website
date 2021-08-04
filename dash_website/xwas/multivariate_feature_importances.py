from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options_from_list
from dash_website import (
    DIMENSIONS_SUBDIMENSIONS,
    DOWNLOAD_CONFIG,
    MAIN_CATEGORIES_TO_CATEGORIES,
    RENAME_DIMENSIONS,
    ALGORITHMS,
    CORRELATION_TYPES,
)
from dash_website.xwas import (
    FEATURES_TABLE_COLUMNS,
    FEATURES_CORRELATIONS_TABLE_COLUMNS,
    MULTIVARIATE_CATEGORIES_TO_REMOVE,
)


@APP.callback(
    Output("memory_features_multivariate", "data"),
    [Input("dimension_subdimension_features_multivariate", "value"), Input("category_features_multivariate", "value")],
)
def _modify_store_features_multivariate(dimension_subdimension, category):
    return load_feather(
        f"xwas/multivariate_feature_importances/dimension_category/features_{RENAME_DIMENSIONS.get(dimension_subdimension, dimension_subdimension)}_{category}.feather"
    ).to_dict()


def get_controls_features_multivariate():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_features_multivariate",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down("category_features_multivariate", ["..."], "Select X subcategory: ", from_dict=False),
            get_drop_down(
                "dimension_subdimension_features_multivariate", DIMENSIONS_SUBDIMENSIONS, "Select an aging dimension: "
            ),
        ]
    )


@APP.callback(
    [Output("category_features_multivariate", "options"), Output("category_features_multivariate", "value")],
    Input("main_category_features_multivariate", "value"),
)
def _change_controls_category_features_multivariate(main_category):
    categories = MAIN_CATEGORIES_TO_CATEGORIES[main_category].copy()

    for category_to_remove in MULTIVARIATE_CATEGORIES_TO_REMOVE:
        if category_to_remove in categories:
            categories.remove(category_to_remove)

    return get_options_from_list(categories), categories[0]


def get_controls_table_features_multivariate():
    return dbc.Card(
        [
            get_item_radio_items(
                "correlation_type_features_multivariate", CORRELATION_TYPES, "Select correlation type :"
            ),
            dbc.FormGroup(
                [
                    html.P("Correlation between feature importances/correlation : "),
                    dash_table.DataTable(
                        id="table_correlation_features_multivariate",
                        columns=[
                            {"id": key, "name": name} for key, name in FEATURES_CORRELATIONS_TABLE_COLUMNS.items()
                        ],
                        style_cell={"textAlign": "left", "fontSize": 10},
                        sort_action="custom",
                        sort_mode="single",
                    ),
                    html.Br(),
                ]
            ),
        ]
    )


@APP.callback(
    [Output("bar_plot_features_multivariate", "figure"), Output("title_features_multivariate", "children")],
    [
        Input("dimension_subdimension_features_multivariate", "value"),
        Input("category_features_multivariate", "value"),
        Input("memory_features_multivariate", "data"),
        Input("memory_scores_features_multivariate", "data"),
    ],
)
def _fill_bar_plot_feature(dimension, category, data_features, data_scores):
    import plotly.graph_objects as go

    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "category"])
    scores = scores_raw.loc[dimension, category]
    best_algorithm = scores.iloc[scores["r2"].argmax()]["algorithm"]

    scores_algorithm = scores.reset_index().set_index("algorithm").round(3)
    title = f"R² : Elastic Net {scores_algorithm.loc['elastic_net', 'r2']} +- {scores_algorithm.loc['elastic_net', 'std']}, "
    title += f"Light GBM {scores_algorithm.loc['light_gbm', 'r2']} +- {scores_algorithm.loc['light_gbm', 'std']}, Neural Network {scores_algorithm.loc['neural_network', 'r2']} +- {scores_algorithm.loc['neural_network', 'std']}"

    features = pd.DataFrame(data_features).set_index(["algorithm", "variable"])
    sorted_variables = (
        (features.loc[best_algorithm].abs() / features.loc[best_algorithm].abs().sum())
        .sort_values(by=["feature_importance"], ascending=False)
        .index
    )

    algorithms = features.index.get_level_values("algorithm").drop_duplicates()

    table_features = pd.DataFrame(None, columns=FEATURES_TABLE_COLUMNS.keys())
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
                name=ALGORITHMS[algorithm],
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
            "xaxis": {
                "title": "Percentage of overall feature importance",
                "showgrid": False,
                "title_font": {"size": 25},
            },
            "yaxis": {"title": "Variables", "showgrid": False, "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    return (fig, title)


@APP.callback(
    [Output("table_features_multivariate", "data"), Output("table_correlation_features_multivariate", "data")],
    [
        Input("dimension_subdimension_features_multivariate", "value"),
        Input("category_features_multivariate", "value"),
        Input("correlation_type_features_multivariate", "value"),
        Input("memory_scores_features_multivariate", "data"),
        Input("memory_features_multivariate", "data"),
        Input("table_features_multivariate", "sort_by"),
        Input("table_correlation_features_multivariate", "sort_by"),
    ],
)
def _sort_tables_features_multivariate(
    dimension, category, correlation_type, data_scores, data_features, sort_by_col_features, sort_by_col_correlations
):
    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "category"])
    if (dimension, category) in scores_raw.index:
        scores = scores_raw.loc[dimension, category]
        best_algorithm = scores.iloc[scores["r2"].argmax()]["algorithm"]
    else:
        best_algorithm = "light_gbm"

    features = pd.DataFrame(data_features).set_index(["algorithm", "variable"])
    sorted_variables = (
        (features.loc[best_algorithm].abs() / features.loc[best_algorithm].abs().sum())
        .sort_values(by=["feature_importance"], ascending=False)
        .index
    )

    algorithms = features.index.get_level_values("algorithm").drop_duplicates()

    table_features = pd.DataFrame(None, columns=FEATURES_TABLE_COLUMNS.keys())
    table_features["variable"] = sorted_variables

    for algorithm in algorithms:
        sorted_algorithm_variable = [[algorithm, variable] for variable in sorted_variables]

        table_features[f"feature_{algorithm}"] = features.loc[sorted_algorithm_variable].values
        table_features[f"percentage_{algorithm}"] = (
            features.loc[sorted_algorithm_variable].abs() / features.loc[sorted_algorithm_variable].abs().sum()
        )["feature_importance"].values

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

    if sort_by_col_features is not None and len(sort_by_col_features) > 0:
        is_ascending = sort_by_col_features[0]["direction"] == "asc"
        table_features.sort_values(sort_by_col_features[0]["column_id"], ascending=is_ascending, inplace=True)
    else:
        table_features.sort_values("feature_light_gbm", inplace=True)

    if sort_by_col_correlations is not None and len(sort_by_col_correlations) > 0:
        is_ascending = sort_by_col_correlations[0]["direction"] == "asc"
        table_correlations.sort_values(sort_by_col_correlations[0]["column_id"], ascending=is_ascending, inplace=True)

    return table_features[FEATURES_TABLE_COLUMNS].round(5).to_dict("records"), table_correlations[
        FEATURES_CORRELATIONS_TABLE_COLUMNS
    ].round(5).to_dict("records")


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_features_multivariate"),
                dcc.Store(
                    id="memory_scores_features_multivariate",
                    data=load_feather(
                        f"xwas/multivariate_results/scores.feather",
                        columns=["category", "dimension", "r2", "std", "algorithm"],
                    ).to_dict(),
                ),
            ]
        ),
        html.H1("Accelerated aging prediction interpretability - XWAS"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_controls_features_multivariate(),
                        html.Br(),
                        html.Br(),
                        get_controls_table_features_multivariate(),
                    ],
                    width={"size": 5},
                ),
                dbc.Col(
                    dcc.Loading(
                        [
                            html.H2(id="title_features_multivariate"),
                            dcc.Graph(id="bar_plot_features_multivariate", config=DOWNLOAD_CONFIG),
                        ]
                    ),
                    width={"size": 7},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Loading(
                        [
                            dash_table.DataTable(
                                id="table_features_multivariate",
                                columns=[{"id": key, "name": name} for key, name in FEATURES_TABLE_COLUMNS.items()],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ]
                    ),
                    width={"size": 8, "offset": 2},
                )
            ]
        ),
    ],
    fluid=True,
)
