from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_options
from dash_website import DOWNLOAD_CONFIG
from dash_website import CORRELATION_TYPES, ALGORITHMS_RENDERING
from dash_website.feature_importances import TREE_SCALARS, FEATURES_TABLE_COLUMNS, FEATURES_CORRELATIONS_TABLE_COLUMNS


def get_data_scores():
    return load_feather("feature_importances/scores_all_samples_per_participant.feather").to_dict()


@APP.callback(
    Output("memory_features", "data"),
    [
        Input("dimension_scalars_features", "value"),
        Input("subdimension_scalars_features", "value"),
        Input("sub_subdimension_scalars_features", "value"),
    ],
)
def _modify_store_features(dimension, subdimension, sub_subdimension):
    return load_feather(f"feature_importances/scalars/{dimension}_{subdimension}_{sub_subdimension}.feather").to_dict()


def get_controls_scalars_features():
    first_dimension = list(TREE_SCALARS.keys())[0]
    first_subdimension = list(TREE_SCALARS[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_scalars_features", list(TREE_SCALARS.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_scalars_features",
            list(TREE_SCALARS[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_item_radio_items(
            "sub_subdimension_scalars_features",
            TREE_SCALARS[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_scalars_features", "options"),
        Output("subdimension_scalars_features", "value"),
        Output("sub_subdimension_scalars_features", "options"),
        Output("sub_subdimension_scalars_features", "value"),
    ],
    [Input("dimension_scalars_features", "value"), Input("subdimension_scalars_features", "value")],
)
def _change_subdimensions_features(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_scalars_features":
        first_subdimension = list(TREE_SCALARS[dimension].keys())[0]
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            list(TREE_SCALARS[dimension].keys())[0],
            get_options(TREE_SCALARS[dimension][first_subdimension]),
            TREE_SCALARS[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            subdimension,
            get_options(TREE_SCALARS[dimension][subdimension]),
            TREE_SCALARS[dimension][subdimension][0],
        )


def get_controls_table_scalars_features():
    return [
        get_item_radio_items(
            "correlation_type_scalars_features",
            CORRELATION_TYPES,
            "Select sub-subdimension :",
        ),
        dbc.FormGroup(
            [
                html.P("Correlation between feature importances/correlation : "),
                dash_table.DataTable(
                    id="table_correlation_scalars_features",
                    columns=[{"id": key, "name": name} for key, name in FEATURES_CORRELATIONS_TABLE_COLUMNS.items()],
                    style_cell={"textAlign": "left"},
                    sort_action="custom",
                    sort_mode="single",
                ),
                html.Br(),
            ]
        ),
    ]


@APP.callback(
    [
        Output("bar_plot_scalars_features", "figure"),
        Output("title_scalars_features", "children"),
        Output("sub_title_scalars_features", "children"),
    ],
    [
        Input("dimension_scalars_features", "value"),
        Input("subdimension_scalars_features", "value"),
        Input("sub_subdimension_scalars_features", "value"),
        Input("memory_scores", "data"),
        Input("memory_features", "data"),
    ],
)
def _fill_bar_plot_feature(dimension, subdimension, sub_subdimension, data_scores, data_features):
    import plotly.graph_objects as go

    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension"]).round(3)
    scores = (
        scores_raw.loc[(dimension, subdimension, sub_subdimension)]
        .set_index("algorithm")
        .sort_values("r2", ascending=False)
    )

    best_algorithm = scores.index[0]
    best_score = scores.loc[best_algorithm]

    title = f"The best algorithm is the {ALGORITHMS_RENDERING[best_algorithm]}. The R2 is {best_score['r2']} +- {best_score['r2_std']} with a RMSE of {best_score['rmse']} +- {best_score['rmse_std']} for a sample size of {int(best_score['sample_size'])} participants"

    other_scores = scores.drop(index=best_algorithm)
    subtitle = ""
    for other_algorithm in other_scores.index:
        subtitle += f"The {ALGORITHMS_RENDERING[other_algorithm]} has a R2 of {other_scores.loc[other_algorithm, 'r2']} +- {other_scores.loc[other_algorithm, 'r2_std']}. "

    features = pd.DataFrame(data_features).set_index("feature")
    features.columns = pd.MultiIndex.from_tuples(
        list(map(eval, features.columns.tolist())), names=["algorithm", "observation"]
    )

    sorted_features = features.abs().sort_values(by=[(best_algorithm, "mean")], ascending=False).index

    table_features = pd.DataFrame(None, columns=FEATURES_TABLE_COLUMNS.keys())
    table_features["feature"] = sorted_features

    for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
        table_features[f"percentage_{algorithm}"] = (
            features.loc[sorted_features, (algorithm, "mean")].round(3).astype(str).values
            + " +- "
            + features.loc[sorted_features, (algorithm, "std")].round(3).astype(str).values
        )

    fig = go.Figure()
    hovertemplate = (
        "Feature: %{y} <br>Percentage of overall feature importance: %{x:.3f} +- %{customdata:.3f}<br><extra></extra>"
    )

    for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
        fig.add_bar(
            name=ALGORITHMS_RENDERING[algorithm],
            x=features.loc[sorted_features, (algorithm, "mean")].abs().values[::-1],
            y=sorted_features[::-1],
            error_x={
                "array": features.loc[sorted_features, (algorithm, "std")].values[::-1],
                "type": "data",
            },
            orientation="h",
            hovertemplate=hovertemplate,
            customdata=features.loc[sorted_features, (algorithm, "std")].values[::-1],
        )

    fig.update_layout(
        {
            "width": 1000,
            "height": int(25 * len(sorted_features)),
            "xaxis": {
                "title": "Percentage of overall feature importance",
                "showgrid": False,
                "title_font": {"size": 25},
            },
            "yaxis": {"title": "Features", "showgrid": False, "title_font": {"size": 25}},
        }
    )

    return (fig, title, subtitle)


@APP.callback(
    [Output("table_scalars_features", "data"), Output("table_correlation_scalars_features", "data")],
    [
        Input("dimension_scalars_features", "value"),
        Input("subdimension_scalars_features", "value"),
        Input("sub_subdimension_scalars_features", "value"),
        Input("correlation_type_scalars_features", "value"),
        Input("memory_scores", "data"),
        Input("memory_features", "data"),
        Input("table_scalars_features", "sort_by"),
        Input("table_correlation_scalars_features", "sort_by"),
    ],
)
def _sort_tables(
    dimension,
    subdimension,
    sub_subdimension,
    correlation_type,
    data_scores,
    data_features,
    sort_by_col_features,
    sort_by_col_correlations,
):
    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension"]).round(3)
    scores = (
        scores_raw.loc[(dimension, subdimension, sub_subdimension)]
        .set_index("algorithm")
        .sort_values("r2", ascending=False)
    )

    best_algorithm = scores.index[0]

    features = pd.DataFrame(data_features).set_index("feature")
    features.columns = pd.MultiIndex.from_tuples(
        list(map(eval, features.columns.tolist())), names=["algorithm", "observation"]
    )

    sorted_features = features.abs().sort_values(by=[(best_algorithm, "mean")], ascending=False).index

    table_features = pd.DataFrame(None, columns=FEATURES_TABLE_COLUMNS.keys())
    table_features["feature"] = sorted_features

    for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
        table_features[f"percentage_{algorithm}"] = (
            features.loc[sorted_features, (algorithm, "mean")].round(3).astype(str).values
            + " +- "
            + features.loc[sorted_features, (algorithm, "std")].round(3).astype(str).values
        )

    table_correlations_raw = pd.DataFrame(
        None, index=features.index, columns=pd.Index(FEATURES_CORRELATIONS_TABLE_COLUMNS.keys()).drop("index")
    )

    for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
        table_correlations_raw[f"percentage_{algorithm}"] = features[(algorithm, "mean")]

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
        table_features.sort_values("percentage_light_gbm", inplace=True)

    if sort_by_col_correlations is not None and len(sort_by_col_correlations) > 0:
        is_ascending = sort_by_col_correlations[0]["direction"] == "asc"
        table_correlations.sort_values(sort_by_col_correlations[0]["column_id"], ascending=is_ascending, inplace=True)

    return table_features[FEATURES_TABLE_COLUMNS].round(3).to_dict("records"), table_correlations[
        FEATURES_CORRELATIONS_TABLE_COLUMNS
    ].round(3).to_dict("records")


LAYOUT = dbc.Container(
    [
        dcc.Loading([dcc.Store(id="memory_features"), dcc.Store(id="memory_scores", data=get_data_scores())]),
        html.H1("Model interpretability - Scalars"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Card(get_controls_scalars_features()),
                        html.Br(),
                        html.Br(),
                        dbc.Card(get_controls_table_scalars_features()),
                    ],
                    width={"size": 5},
                ),
                dbc.Col(
                    dcc.Loading(
                        [
                            html.H3(id="title_scalars_features"),
                            html.H5(id="sub_title_scalars_features"),
                            dcc.Graph(id="bar_plot_scalars_features", config=DOWNLOAD_CONFIG),
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
                                id="table_scalars_features",
                                columns=[{"id": key, "name": name} for key, name in FEATURES_TABLE_COLUMNS.items()],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ]
                    ),
                    width={"size": 8, "offset": 3},
                )
            ]
        ),
    ],
    fluid=True,
)
