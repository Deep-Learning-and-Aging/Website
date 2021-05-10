from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down
from dash_website.utils.graphs import (
    heatmap_by_clustering,
    heatmap_by_sorted_dimensions,
    add_line_and_annotation,
    histogram_correlation,
)
from dash_website import DOWNLOAD_CONFIG, ORDER_TYPES, CUSTOM_ORDER
from dash_website.correlation_between import SAMPLE_DEFINITION


def get_all_dimensions():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_all_dimensions")),
            html.H1("Correlation between accelerated aging dimensions"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_all_dimensions(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_all_dimensions"),
                                    dcc.Graph(id="graph_all_dimensions", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 9},
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H4("Histogram of the above correlations"),
                                    dcc.Graph(id="histogram_all_dimensions", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 6, "offset": 3},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


@APP.callback(
    Output("memory_all_dimensions", "data"),
    Input("sample_definition_all_dimensions", "value"),
)
def _modify_store_all_dimensions(sample_definition):
    return load_feather(
        f"correlation_between_accelerated_aging_dimensions/all_dimensions_{sample_definition}.feather"
    ).to_dict()


def get_controls_tab_all_dimensions():
    return dbc.Card(
        [
            get_item_radio_items(
                "sample_definition_all_dimensions", SAMPLE_DEFINITION, "Select the way we define a sample: "
            ),
            get_item_radio_items("order_type_all_dimensions", ORDER_TYPES, "Order by:"),
            get_drop_down(
                "dimension_all_dimensions",
                ["all"] + list(pd.Index(CUSTOM_ORDER).drop(["*", "*instances01", "*instances1.5x", "*instances23"])),
                "Select an aging dimension: ",
                from_dict=False,
            ),
        ]
    )


@APP.callback(
    [
        Output("graph_all_dimensions", "figure"),
        Output("title_all_dimensions", "children"),
        Output("histogram_all_dimensions", "figure"),
    ],
    [
        Input("order_type_all_dimensions", "value"),
        Input("dimension_all_dimensions", "value"),
        Input("memory_all_dimensions", "data"),
    ],
)
def _fill_graph_tab_all_dimensions(order_by, selected_dimension, data_all_dimensions):
    correlations = pd.DataFrame(data_all_dimensions)
    if selected_dimension != "all":
        correlations = correlations[
            (correlations["dimension_1"] == selected_dimension) & (correlations["dimension_2"] == selected_dimension)
        ]

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"],
        columns=["dimension_2", "subdimension_2", "sub_subdimension_2", "algorithm_2"],
        values="correlation",
    )

    customdata_list = []
    for customdata_item in ["correlation_std", "r2_1", "r2_std_1", "r2_2", "r2_std_2"]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"],
                columns=["dimension_2", "subdimension_2", "sub_subdimension_2", "algorithm_2"],
                values=customdata_item,
            ).values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=table_correlations.index, columns=table_correlations.columns)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>r2: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>Dimensions 2: %{y} <br>r2: %{customdata[3]:.3f} +- %{customdata[4]:.3f}<br><extra></extra>"

    if order_by == "clustering":
        fig = heatmap_by_clustering(table_correlations, hovertemplate, customdata)

    elif order_by == "r2":
        sorted_dimensions = (
            correlations.set_index(["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"])
            .sort_values(by="r2_1", ascending=False)
            .index.drop_duplicates()
        )

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

    else:  # order_by == "custom"
        if selected_dimension == "all":
            sorted_dimensions = (
                correlations.set_index(["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"])
                .loc[CUSTOM_ORDER]
                .index.drop_duplicates()
            )
        else:
            sorted_dimensions = [selected_dimension]

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

        fig.update_layout(
            xaxis={"tickvals": np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10)},
            yaxis={"tickvals": np.arange(5, 10 * sorted_table_correlations.shape[0] + 5, 10)},
        )

        dimensions = (
            sorted_table_correlations.index.to_frame()[["dimension_1", "subdimension_1", "sub_subdimension_1"]]
            .reset_index(drop=True)
            .rename(
                columns={
                    "dimension_1": "dimension",
                    "subdimension_1": "subdimension",
                    "sub_subdimension_1": "sub_subdimension",
                }
            )
        )
        dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
        dimensions.set_index(["dimension", "subdimension", "sub_subdimension"], inplace=True)

        lines = []
        annotations = []

        if selected_dimension == "all":
            dimension_outer_margin = -800
            dimension_inner_margin = -400
            subdimension_margin = 0
        else:
            dimension_outer_margin = -500
            dimension_inner_margin = -400
            subdimension_margin = -200
            sub_subdimension_margin = 0

        textangles = {"x": 90, "y": 0}

        for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
            min_position = dimensions.loc[dimension].min()
            max_position = dimensions.loc[dimension].max()

            for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                line, annotation = add_line_and_annotation(
                    dimension,
                    first_axis,
                    second_axis,
                    min_position,
                    max_position,
                    dimension_inner_margin,
                    dimension_outer_margin,
                    textangles[first_axis],
                    10,
                )

                lines.append(line)
                annotations.append(annotation)

                for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
                    submin_position = dimensions.loc[(dimension, subdimension)].min()
                    submax_position = dimensions.loc[(dimension, subdimension)].max()

                    for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                        line, annotation = add_line_and_annotation(
                            subdimension,
                            first_axis,
                            second_axis,
                            submin_position,
                            submax_position,
                            subdimension_margin,
                            dimension_inner_margin,
                            textangles[first_axis],
                            8,
                        )

                        lines.append(line)
                        annotations.append(annotation)

                        if selected_dimension == "all":
                            continue

                        for sub_subdimension in (
                            dimensions.loc[(dimension, subdimension)]
                            .index.get_level_values("sub_subdimension")
                            .drop_duplicates()
                        ):
                            sub_submin_position = dimensions.loc[(dimension, subdimension, sub_subdimension)].min()
                            sub_submax_position = dimensions.loc[(dimension, subdimension, sub_subdimension)].max()

                            for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                                line, annotation = add_line_and_annotation(
                                    sub_subdimension,
                                    first_axis,
                                    second_axis,
                                    sub_submin_position,
                                    sub_submax_position,
                                    sub_subdimension_margin,
                                    subdimension_margin,
                                    textangles[first_axis],
                                    8,
                                )

                                lines.append(line)
                                annotations.append(annotation)

        # The final top/right line
        for first_axis, second_axis in [("x", "y"), ("y", "x")]:
            line, _ = add_line_and_annotation(
                dimension,
                first_axis,
                second_axis,
                min_position,
                max_position,
                0,
                dimension_outer_margin,
                0,
                10,
                final=True,
            )

            lines.append(line)

        fig["layout"]["shapes"] = lines
        fig["layout"]["annotations"] = annotations

    if selected_dimension == "all" or order_by == "custom":
        fig.update_layout(yaxis={"showticklabels": False}, xaxis={"showticklabels": False})
    else:
        fig.update_layout(font={"size": 8})

    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False},
        xaxis={"showgrid": False, "zeroline": False},
        width=1100,
        height=1100,
    )

    return (
        fig,
        f"Average correlation = {correlations['correlation'].mean().round(3)} +- {correlations['correlation'].std().round(3)}",
        histogram_correlation(table_correlations),
    )
