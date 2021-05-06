from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items
from dash_website.utils.graphs.add_line_and_annotation import add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG
from dash_website.utils import BLUE_WHITE_RED
from dash_website.correlation_between import ORDER_TYPES, CUSTOM_ORDER


def get_layout():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_genetics_correlations", data=get_data())),
            html.H1("Genetics - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_genetics_correlations(),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_genetics_correlations"),
                                    dcc.Graph(id="graph_genetics_correlations", config=DOWNLOAD_CONFIG),
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


def get_data():
    return load_feather(f"genetics/correlations/correlations.feather").to_dict()


def get_controls_tab_genetics_correlations():
    return dbc.Card(get_item_radio_items("order_type_genetics_correlations", ORDER_TYPES, "Order by:"))


@APP.callback(
    [Output("graph_genetics_correlations", "figure"), Output("title_genetics_correlations", "children")],
    [
        Input("order_type_genetics_correlations", "value"),
        Input("memory_genetics_correlations", "data"),
    ],
)
def _fill_graph_tab_custom_dimensions(order_by, data_genetics_correlations):
    from dash_website.utils.graphs.dendrogram_heatmap import create_dendrogram_heatmap
    import plotly.graph_objs as go

    correlations = pd.DataFrame(data_genetics_correlations)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    )

    customdata_list = []
    for customdata_item in [
        "correlation_std",
        "r2_1",
        "r2_std_1",
        "h2_1",
        "h2_std_1",
        "r2_2",
        "r2_std_2",
        "h2_2",
        "h2_std_2",
    ]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            ).values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=table_correlations.index, columns=table_correlations.columns)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>r²: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>h²: %{customdata[3]:.3f} +- %{customdata[4]:.3f} <br>Dimensions 2: %{y}<br>r²: %{customdata[5]:.3f} +- %{customdata[6]:.3f}<br>h²: %{customdata[7]:.3f} +- %{customdata[8]:.3f}<br><extra></extra>"

    if order_by == "clustering" or 0 != 0:
        fig = create_dendrogram_heatmap(table_correlations, hovertemplate, customdata)
    elif order_by == "r2" or 0 != 0:
        sorted_dimensions = (
            correlations.set_index(["dimension_1", "subdimension_1"])
            .sort_values(by="r2_1", ascending=False)
            .index.drop_duplicates()
        )

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        heatmap = go.Heatmap(
            x=[" - ".join(elem) for elem in sorted_table_correlations.columns.values],
            y=[" - ".join(elem) for elem in sorted_table_correlations.index.values],
            z=sorted_table_correlations,
            colorscale=BLUE_WHITE_RED,
            customdata=sorted_customdata,
            hovertemplate=hovertemplate,
            zmin=-1,
            zmax=1,
        )

        fig = go.Figure(heatmap)

    else:  # order_by == "custom"
        sorted_dimensions = (
            correlations.set_index(["dimension_1", "subdimension_1"]).loc[CUSTOM_ORDER].index.drop_duplicates()
        )

        sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
        sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

        heatmap = go.Heatmap(
            x=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
            y=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
            z=sorted_table_correlations,
            colorscale=BLUE_WHITE_RED,
            customdata=sorted_customdata,
            hovertemplate=hovertemplate,
            zmin=-1,
            zmax=1,
        )

        fig = go.Figure(heatmap)

        fig.update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
                "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.columns.values],
            },
            yaxis={
                "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[0] + 5, 10),
                "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.index.values],
            },
        )

        dimensions = (
            sorted_table_correlations.index.to_frame()[["dimension_1", "subdimension_1"]]
            .reset_index(drop=True)
            .rename(columns={"dimension_1": "dimension", "subdimension_1": "subdimension"})
        )
        dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
        dimensions.set_index(["dimension", "subdimension"], inplace=True)

        lines = []
        annotations = []

        for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
            dimension_inner_margin = -30
            dimension_outer_margin = -60

            min_position = dimensions.loc[dimension].min()
            max_position = dimensions.loc[dimension].max()

            for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                if first_axis == "x":
                    textangle = 90
                else:  # first_axis == "y"
                    textangle = 0

                line, annotation = add_line_and_annotation(
                    dimension,
                    first_axis,
                    second_axis,
                    min_position,
                    max_position,
                    dimension_inner_margin,
                    dimension_outer_margin,
                    textangle,
                    10,
                )

                lines.append(line)
                annotations.append(annotation)

                for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
                    subdimension_inner_margin = 0
                    subdimension_outer_margin = -30

                    submin_position = dimensions.loc[(dimension, subdimension)].min()
                    submax_position = dimensions.loc[(dimension, subdimension)].max()

                    for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                        if first_axis == "x":
                            textangle = 90
                        else:  # first_axis == "y"
                            textangle = 0

                        line, annotation = add_line_and_annotation(
                            subdimension,
                            first_axis,
                            second_axis,
                            submin_position,
                            submax_position,
                            subdimension_inner_margin,
                            subdimension_outer_margin,
                            textangle,
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
        fig.update_layout(yaxis={"showticklabels": False}, xaxis={"showticklabels": False})

    if order_by != "custom":
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
    )
