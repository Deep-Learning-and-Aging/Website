from botocore.exceptions import IncompleteReadError
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items, get_options_from_list
from dash_website.utils.graphs import add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG, ALGORITHMS, CUSTOM_DIMENSIONS, SCORES
from dash_website.age_prediction_performances import SAMPLE_DEFINITION, DIMENSIONS_SELECTION


@APP.callback(
    Output("memory_age_prediction_performances", "data"),
    Input("sample_definition_age_prediction_performances", "value"),
)
def _get_data_age_prediction_performances(sample_definition):
    return load_feather(f"age_prediction_performances/scores_{sample_definition}.feather").to_dict()


def get_controls_age_prediction_performances():
    return dbc.Card(
        [
            get_item_radio_items(
                "sample_definition_age_prediction_performances",
                SAMPLE_DEFINITION,
                "Select the way we define a sample: ",
            ),
            get_item_radio_items(
                "dimensions_selection_age_prediction_performances",
                DIMENSIONS_SELECTION,
                "Filter models: ",
            ),
            get_drop_down(
                "selected_dimension_age_prediction_performances",
                ["all"] + CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates().tolist(),
                "Select an aging dimension: ",
                from_dict=False,
            ),
            get_item_radio_items(
                "metric_age_prediction_performances",
                SCORES,
                "Select a metric: ",
            ),
        ]
    )


@APP.callback(
    [
        Output("selected_dimension_age_prediction_performances", "options"),
        Output("selected_dimension_age_prediction_performances", "value"),
    ],
    Input("dimensions_selection_age_prediction_performances", "value"),
)
def _change_dimensions_age_prediction_performances(dimensions_selection):
    if dimensions_selection != "without_ensemble_models":
        return (
            get_options_from_list(["all"] + CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates().tolist()),
            "all",
        )
    else:
        return (
            get_options_from_list(
                ["all"]
                + CUSTOM_DIMENSIONS.get_level_values("dimension")
                .drop_duplicates()
                .drop(["*", "*instances01", "*instances1.5x", "*instances23"])
                .tolist()
            ),
            "all",
        )


@APP.callback(
    [Output("graph_age_prediction_performances", "figure"), Output("title_age_prediction_performances", "children")],
    [
        Input("dimensions_selection_age_prediction_performances", "value"),
        Input("selected_dimension_age_prediction_performances", "value"),
        Input("metric_age_prediction_performances", "value"),
        Input("memory_age_prediction_performances", "data"),
    ],
)
def _fill_graph_age_prediction_performances(
    dimensions_selection, selected_dimension, metric, data_age_prediction_performances
):
    import plotly.graph_objs as go

    scores = pd.DataFrame(data_age_prediction_performances)

    if dimensions_selection == "custom_dimensions":
        scores.set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"], inplace=True)
        scores.drop(index=scores.index[~scores.index.isin(CUSTOM_DIMENSIONS)], inplace=True)
        scores.reset_index(inplace=True)
    elif dimensions_selection == "without_ensemble_models":
        scores.drop(
            index=scores.index[
                (scores["dimension"] == "*") | (scores["subdimension"] == "*") | (scores["sub_subdimension"] == "*")
            ],
            inplace=True,
        )
    scores.set_index(["dimension", "subdimension", "sub_subdimension"], inplace=True)

    if selected_dimension != "all":
        scores = scores.loc[[selected_dimension]]

    sorted_dimensions = scores.index.drop_duplicates()

    x_positions = pd.DataFrame(
        np.arange(5, 10 * len(sorted_dimensions) + 5, 10), index=sorted_dimensions, columns=["x_position"]
    )

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(sorted_dimensions) + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_dimensions.values],
        }
    )

    algorithms = scores["algorithm"].drop_duplicates()

    hovertemplate = (
        "%{x}, score: %{y:.3f} +- %{customdata[0]:.3f}, sample size: %{customdata[1]} <extra>%{customdata[2]}</extra>"
    )

    min_score = min(scores[metric].min(), 0)

    for algorithm in algorithms:
        scores_algorithm = scores[scores["algorithm"] == algorithm]
        x_positions.loc[scores_algorithm.index]

        customdata = np.dstack(
            (
                scores_algorithm[f"{metric}_std"].values.flatten(),
                scores_algorithm["sample_size"].values.flatten(),
                [algorithm] * len(scores_algorithm.index),
            )
        )[0]
        fig.add_bar(
            x=x_positions.loc[scores_algorithm.index].values.flatten(),
            y=scores_algorithm[metric],
            error_y={"array": scores_algorithm[f"{metric}_std"], "type": "data"},
            name=ALGORITHMS[algorithm],
            hovertemplate=hovertemplate,
            customdata=customdata,
        )

    dimensions = sorted_dimensions.to_frame()[["dimension", "subdimension", "sub_subdimension"]].reset_index(drop=True)
    dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
    dimensions.set_index(["dimension", "subdimension", "sub_subdimension"], inplace=True)

    lines = []
    annotations = []

    if dimensions_selection == "custom_dimensions":
        size_dimension = 18
        size_subdimension = 15
        if metric == "rsme":
            dimension_outer_margin = min_score - 9
            dimension_inner_margin = min_score - 5
            subdimension_margin = min_score - 1
            sub_subdimension_margin = min_score - 1
        else:
            dimension_outer_margin = min_score - 0.9
            dimension_inner_margin = min_score - 0.5
            subdimension_margin = min_score - 0.1
            sub_subdimension_margin = min_score - 0.1

    else:
        if selected_dimension == "all":
            size_dimension = 15
            size_subdimension = 12
            size_sub_subdimension = 11
        else:
            size_dimension = 21
            size_subdimension = 20
            size_sub_subdimension = 20

        if metric == "rmse":
            dimension_outer_margin = min_score - 17
            dimension_inner_margin = min_score - 13
            subdimension_margin = min_score - 9
            sub_subdimension_margin = min_score - 1
        else:
            dimension_outer_margin = min_score - 1.7
            dimension_inner_margin = min_score - 1.3
            subdimension_margin = min_score - 0.9
            sub_subdimension_margin = min_score - 0.1

    for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
        min_position = dimensions.loc[dimension].min()
        max_position = dimensions.loc[dimension].max()

        line, annotation = add_line_and_annotation(
            dimension,
            min_position,
            max_position,
            dimension_inner_margin,
            dimension_outer_margin,
            size_dimension,
            True
        )

        lines.append(line)
        annotations.append(annotation)

        for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
            submin_position = dimensions.loc[(dimension, subdimension)].min()
            submax_position = dimensions.loc[(dimension, subdimension)].max()

            line, annotation = add_line_and_annotation(
                subdimension,
                submin_position,
                submax_position,
                subdimension_margin,
                dimension_inner_margin,
                size_subdimension,
                True,
            )

            lines.append(line)
            annotations.append(annotation)

            if dimensions_selection == "custom_dimensions":
                continue

            for sub_subdimension in (
                dimensions.loc[(dimension, subdimension)].index.get_level_values("sub_subdimension").drop_duplicates()
            ):
                sub_submin_position = dimensions.loc[(dimension, subdimension, sub_subdimension)].min()
                sub_submax_position = dimensions.loc[(dimension, subdimension, sub_subdimension)].max()

                line, annotation = add_line_and_annotation(
                    sub_subdimension,
                    sub_submin_position,
                    sub_submax_position,
                    sub_subdimension_margin,
                    subdimension_margin,
                    size_sub_subdimension,
                    True,
                )

                lines.append(line)
                annotations.append(annotation)

    # The final top/right line
    line, _ = add_line_and_annotation(
        dimension,
        min_position,
        max_position,
        sub_subdimension_margin,
        dimension_outer_margin,
        10,
        True,
        final=True,
    )

    lines.append(line)

    fig["layout"]["shapes"] = lines
    fig["layout"]["annotations"] = annotations
    fig.update_layout(xaxis={"showticklabels": False})

    fig.update_layout(
        yaxis={
            "title": SCORES[metric],
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 45},
            "dtick": 1 if metric == "rmse" else 0.1,
            "tickfont_size": 20,
        },
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        legend={"orientation": "h", "yanchor": "bottom", "font": {"size": 30}},
    )

    return (
        fig,
        f"Average {SCORES[metric]} = {scores[metric].mean().round(3)} +- {scores[metric].std().round(3)}",
    )


LAYOUT = dbc.Container(
    [
        dcc.Loading(dcc.Store(id="memory_age_prediction_performances")),
        html.H1("Age prediction performances"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_controls_age_prediction_performances(),
                        html.Br(),
                        html.Br(),
                    ],
                    width={"size": 3},
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H2(id="title_age_prediction_performances"),
                                dcc.Graph(id="graph_age_prediction_performances", config=DOWNLOAD_CONFIG),
                            ]
                        )
                    ],
                    width={"size": 9},
                ),
            ]
        ),
    ],
    fluid=True,
)
