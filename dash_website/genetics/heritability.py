from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items
from dash_website.utils.graphs import add_line_and_annotation, add_custom_legend_axis
from dash_website import DIMENSIONS_SUBDIMENSIONS_INDEXES, DOWNLOAD_CONFIG
from dash_website.genetics import ORDER_TYPES_HERITABILITY


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

    custom_dimensions = DIMENSIONS_SUBDIMENSIONS_INDEXES.drop([("*", "*"), ("*instances01", "*"), ("Eyes", "All")])

    heritability = pd.DataFrame(data_heritability).set_index(["dimension", "subdimension"]).loc[custom_dimensions]

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
        bars = go.Bar(
            x=np.arange(5, 10 * heritability.shape[0] + 5, 10),
            y=heritability["h2"],
            error_y={"array": heritability["h2_std"], "type": "data"},
            name="Heritability",
            marker_color="indianred",
        )

        fig = go.Figure(bars)

        fig.update_layout(
            xaxis={
                "tickvals": np.arange(5, 10 * heritability.shape[0] + 5, 10),
                "ticktext": [" - ".join(elem) for elem in custom_dimensions.values],
            },
        )

        add_custom_legend_axis(
            fig,
            heritability.index,
            outer_margin_level_1=-0.5,
            inner_margin_level_1=-0.25,
            size_level_1=15,
            size_level_2=10,
        )

    fig.update_layout(
        yaxis={"title": "GWAS-based heritability", "showgrid": False, "zeroline": False, "title_font": {"size": 25}},
        xaxis={"showgrid": False, "zeroline": False},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return (
        fig,
        f"Average heritability = {heritability['h2'].mean().round(3)} +- {heritability['h2'].std().round(3)}",
    )


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            dcc.Store(
                id="memory_heritability", data=load_feather("genetics/heritability/heritability.feather").to_dict()
            )
        ),
        html.H1("Heritability - GWAS"),
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
