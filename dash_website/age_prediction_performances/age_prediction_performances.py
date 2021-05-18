from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather, load_src_image
from dash_website.utils.controls import get_drop_down, get_item_radio_items, get_options
from dash_website.utils.graphs import add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG, CUSTOM_ORDER
from dash_website.age_prediction_performances import SAMPLE_DEFINITION, DIMENSIONS_SELECTION, SCORES


@APP.callback(
    Output("memory_age_prediction_performances", "data"),
    [
        Input("sample_definition_age_prediction_performances", "value"),
        Input("dimensions_selection_age_prediction_performances", "value"),
    ],
)
def _get_data_age_prediction_performances(sample_definition, dimensions_selection):
    return load_feather(
        f"age_prediction_performances/scores_{sample_definition}_{dimensions_selection}.feather"
    ).to_dict()


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
                "Select a group of dimensions: ",
            ),
            get_drop_down(
                "selected_dimension_age_prediction_performances",
                ["all"] + CUSTOM_ORDER,
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
        return get_options(["all"] + CUSTOM_ORDER), "all"
    else:
        return (
            get_options(
                ["all"] + list(pd.Index(CUSTOM_ORDER).drop(["*", "*instances01", "*instances1.5x", "*instances23"]))
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
        scores.replace("1DCNN", "*", inplace=True)  # since it is the only one that is different

    scores.set_index(["dimension", "subdimension", "sub_subdimension"], inplace=True)

    if selected_dimension != "all":
        scores = scores.loc[[selected_dimension]]
        sorted_dimensions = scores.loc[[selected_dimension]].index.drop_duplicates()
    else:
        if dimensions_selection != "without_ensemble_models":
            sorted_dimensions = scores.loc[CUSTOM_ORDER].index.drop_duplicates()
        else:
            sorted_dimensions = scores.loc[
                pd.Index(CUSTOM_ORDER).drop(["*", "*instances01", "*instances1.5x", "*instances23"])
            ].index.drop_duplicates()

    x_positions = pd.DataFrame(
        np.arange(5, 10 * len(sorted_dimensions) + 5, 10), index=sorted_dimensions, columns=["x_position"]
    )

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(sorted_dimensions) + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_dimensions.values],
        },
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
            name=algorithm,
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
        if metric == "r2":
            dimension_outer_margin = min_score - 0.9
            dimension_inner_margin = min_score - 0.5
            subdimension_margin = min_score - 0.1
            sub_subdimension_margin = min_score - 0.1
        else:
            dimension_outer_margin = min_score - 9
            dimension_inner_margin = min_score - 5
            subdimension_margin = min_score - 1
            sub_subdimension_margin = min_score - 1
    else:
        size_dimension = 13
        size_subdimension = 11
        size_sub_subdimension = 9
        if metric == "r2":
            dimension_outer_margin = min_score - 1.4
            dimension_inner_margin = min_score - 1
            subdimension_margin = min_score - 0.6
            sub_subdimension_margin = min_score - 0.1

        else:
            dimension_outer_margin = min_score - 14
            dimension_inner_margin = min_score - 10
            subdimension_margin = min_score - 6
            sub_subdimension_margin = min_score - 1

    for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
        min_position = dimensions.loc[dimension].min()
        max_position = dimensions.loc[dimension].max()

        line, annotation = add_line_and_annotation(
            dimension,
            "x",
            "y",
            min_position,
            max_position,
            dimension_inner_margin,
            dimension_outer_margin,
            90,
            size_dimension,
        )

        lines.append(line)
        annotations.append(annotation)

        for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
            submin_position = dimensions.loc[(dimension, subdimension)].min()
            submax_position = dimensions.loc[(dimension, subdimension)].max()

            line, annotation = add_line_and_annotation(
                subdimension,
                "x",
                "y",
                submin_position,
                submax_position,
                subdimension_margin,
                dimension_inner_margin,
                90,
                size_subdimension,
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
                    "x",
                    "y",
                    sub_submin_position,
                    sub_submax_position,
                    sub_subdimension_margin,
                    subdimension_margin,
                    90,
                    size_sub_subdimension,
                )

                lines.append(line)
                annotations.append(annotation)

    # The final top/right line
    line, _ = add_line_and_annotation(
        dimension,
        "x",
        "y",
        min_position,
        max_position,
        sub_subdimension_margin,
        dimension_outer_margin,
        0,
        10,
        final=True,
    )

    lines.append(line)

    fig["layout"]["shapes"] = lines
    fig["layout"]["annotations"] = annotations
    fig.update_layout(xaxis={"showticklabels": False})

    fig.update_layout(
        yaxis={"title": SCORES[metric], "showgrid": False, "zeroline": False, "title_font": {"size": 25}},
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
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
