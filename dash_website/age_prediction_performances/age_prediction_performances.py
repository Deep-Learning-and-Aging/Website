from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items
from dash_website.utils.graphs.add_line_and_annotation import add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG, CUSTOM_ORDER
from dash_website.age_prediction_performances import SAMPLE_DEFINITION, DIMENSIONS_SELECTION, SCORES


def get_layout():
    return dbc.Container(
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
                        md=3,
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
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


@APP.callback(
    [Output("graph_age_prediction_performances", "figure"), Output("title_age_prediction_performances", "children")],
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
                "dimension_age_prediction_performances",
                ["all"] + CUSTOM_ORDER,
                "Select an aging dimension: ",
                from_dict=False,
            ),
            get_item_radio_items(
                "score_age_prediction_performances",
                SCORES,
                "Select a metric: ",
            ),
        ]
    )


@APP.callback(
    [Output("graph_age_prediction_performances", "figure"), Output("title_age_prediction_performances", "children")],
    [
        Input("order_type_heritability", "value"),
        Input("memory_age_prediction_performances", "data"),
    ],
)
def _fill_graph_heritability(order_by, data_age_prediction_performances):
    pass
    # import plotly.graph_objs as go

    # heritability = pd.DataFrame(data_heritability).set_index(["dimension", "subdimension"])

    # if order_by == "h2":
    #     sorted_dimensions = heritability.sort_values(by="h2", ascending=False).index

    #     sorted_heritability = heritability.loc[sorted_dimensions]

    #     bars = go.Bar(
    #         x=[" - ".join(elem) for elem in sorted_dimensions.values],
    #         y=sorted_heritability["h2"],
    #         error_y={"array": sorted_heritability["h2_std"], "type": "data"},
    #         name="Heritability",
    #         marker_color="indianred",
    #     )

    #     fig = go.Figure(bars)
    #     fig.update_layout(font={"size": 15})

    # else:  # order_by == "custom"
    #     sorted_dimensions = heritability.loc[pd.Index(CUSTOM_ORDER).drop(["*", "*instances01"])].index

    #     sorted_heritability = heritability.loc[sorted_dimensions]

    #     bars = go.Bar(
    #         x=np.arange(5, 10 * sorted_heritability.shape[0] + 5, 10),
    #         y=sorted_heritability["h2"],
    #         error_y={"array": sorted_heritability["h2_std"], "type": "data"},
    #         name="Heritability",
    #         marker_color="indianred",
    #     )

    #     fig = go.Figure(bars)

    #     fig.update_layout(
    #         xaxis={
    #             "tickvals": np.arange(5, 10 * sorted_heritability.shape[0] + 5, 10),
    #             "ticktext": [" - ".join(elem) for elem in sorted_dimensions.values],
    #         },
    #     )

    #     dimensions = sorted_heritability.index.to_frame()[["dimension", "subdimension"]].reset_index(drop=True)
    #     dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
    #     dimensions.set_index(["dimension", "subdimension"], inplace=True)

    #     lines = []
    #     annotations = []

    #     for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
    #         dimension_inner_margin = -0.25
    #         dimension_outer_margin = -0.5

    #         min_position = dimensions.loc[dimension].min()
    #         max_position = dimensions.loc[dimension].max()

    #         line, annotation = add_line_and_annotation(
    #             dimension,
    #             "x",
    #             "y",
    #             min_position,
    #             max_position,
    #             dimension_inner_margin,
    #             dimension_outer_margin,
    #             90,
    #             18,
    #         )

    #         lines.append(line)
    #         annotations.append(annotation)

    #         for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
    #             subdimension_inner_margin = 0
    #             subdimension_outer_margin = -0.25

    #             submin_position = dimensions.loc[(dimension, subdimension)].min()
    #             submax_position = dimensions.loc[(dimension, subdimension)].max()

    #             line, annotation = add_line_and_annotation(
    #                 subdimension,
    #                 "x",
    #                 "y",
    #                 submin_position,
    #                 submax_position,
    #                 subdimension_inner_margin,
    #                 subdimension_outer_margin,
    #                 90,
    #                 15,
    #             )

    #             lines.append(line)
    #             annotations.append(annotation)

    #     # The final top/right line
    #     line, _ = add_line_and_annotation(
    #         dimension,
    #         "x",
    #         "y",
    #         min_position,
    #         max_position,
    #         0,
    #         dimension_outer_margin,
    #         0,
    #         10,
    #         final=True,
    #     )

    #     lines.append(line)

    #     fig["layout"]["shapes"] = lines
    #     fig["layout"]["annotations"] = annotations
    #     fig.update_layout(xaxis={"showticklabels": False})

    # fig.update_layout(
    #     yaxis={"showgrid": False, "zeroline": False},
    #     xaxis={"showgrid": False, "zeroline": False},
    #     height=800,
    # )

    # return (
    #     fig,
    #     f"Average heritability = {heritability['h2'].mean().round(3)} +- {heritability['h2'].std().round(3)}",
    # )
