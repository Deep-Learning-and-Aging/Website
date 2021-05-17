from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items
from dash_website.utils.graphs import add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG, CUSTOM_ORDER
from dash_website.genetics import ORDER_TYPES_HERITABILITY


def get_data():
    return load_feather(f"genetics/heritability/heritability.feather").to_dict()


def get_controls_heritability():
    return dbc.Card(get_item_radio_items("order_type_heritability", ORDER_TYPES_HERITABILITY, "Order by:"))


@APP.callback(
    [Output("graph_heritability", "figure"), Output("title_heritability", "children")],
    [
        Input("order_type_heritability", "value"),
        Input("memory_heritability", "data"),
    ],
)
def _fill_graph_heritability(order_by, data_heritability):
    import plotly.graph_objs as go

    heritability = pd.DataFrame(data_heritability).set_index(["dimension", "subdimension"])

    if order_by == "h2":
        sorted_dimensions = heritability.sort_values(by="h2", ascending=False).index

        sorted_heritability = heritability.loc[sorted_dimensions]

        bars = go.Bar(
            x=[" - ".join(elem) for elem in sorted_dimensions.values],
            y=sorted_heritability["h2"],
            error_y={"array": sorted_heritability["h2_std"], "type": "data"},
            name="Heritability",
            marker_color="indianred",
        )

        fig = go.Figure(bars)
        fig.update_layout(font={"size": 15})

    else:  # order_by == "custom"
        sorted_dimensions = heritability.loc[pd.Index(CUSTOM_ORDER).drop(["*", "*instances01"])].index

        sorted_heritability = heritability.loc[sorted_dimensions]

        bars = go.Bar(
            x=np.arange(5, 10 * sorted_heritability.shape[0] + 5, 10),
            y=sorted_heritability["h2"],
            error_y={"array": sorted_heritability["h2_std"], "type": "data"},
            name="Heritability",
            marker_color="indianred",
        )

        fig = go.Figure(bars)

        fig.update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * sorted_heritability.shape[0] + 5, 10),
                "ticktext": [" - ".join(elem) for elem in sorted_dimensions.values],
            },
        )

        dimensions = sorted_heritability.index.to_frame()[["dimension", "subdimension"]].reset_index(drop=True)
        dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
        dimensions.set_index(["dimension", "subdimension"], inplace=True)

        lines = []
        annotations = []

        for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
            dimension_inner_margin = -0.25
            dimension_outer_margin = -0.5

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
                18,
            )

            lines.append(line)
            annotations.append(annotation)

            for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
                subdimension_margin = 0

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
                    15,
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
            0,
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
        yaxis={"title": "GWAS-based heritability", "showgrid": False, "zeroline": False, "title_font": {"size": 25}},
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
    )

    return (
        fig,
        f"Average heritability = {heritability['h2'].mean().round(3)} +- {heritability['h2'].std().round(3)}",
    )


LAYOUT = dbc.Container(
    [
        dcc.Loading(dcc.Store(id="memory_heritability", data=get_data())),
        html.H1("Genetics - Heritabiliy"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_controls_heritability(),
                        html.Br(),
                        html.Br(),
                    ],
                    width={"size": 3},
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H2(id="title_heritability"),
                                dcc.Graph(id="graph_heritability", config=DOWNLOAD_CONFIG),
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
