from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import (
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
    get_dimension_drop_down,
)
from dash_website import DIMENSIONS


def get_dimension_heatmap():
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [
                            html.H2(id="title_dimension"),
                            dcc.Graph(id="graph_dimension"),
                        ],
                        style={"overflowY": "scroll", "height": 1000, "overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab():
    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension", DIMENSIONS),
            get_subset_method_radio_items("subset_method_correlations"),
            get_correlation_type_radio_items("correlation_type_dimension"),
        ]
    )


@APP.callback(
    [Output("graph_dimension", "figure"), Output("title_dimension", "children")],
    [
        Input("dimension_dimension", "value"),
        Input("correlation_type_dimension", "value"),
        Input("memory_correlations", "data"),
    ],
)
def _fill_graph_tab_organ(dimension, correlation_type, data):
    from dash_website.utils.graphs.colorscale import get_colorscale
    import plotly.graph_objs as go

    correlations = pd.DataFrame(data).set_index(["dimension_1", "dimension_2", "category"])
    correlations.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations.columns.tolist())), names=["subset_method", "observation"]
    )

    if dimension == DIMENSIONS[-1]:
        correlations_2d_1 = None
        number_variables_2d_1 = None
    else:
        matrix_correlations_2d_1 = correlations[correlation_type].loc[dimension, "mean"].swaplevel()
        matrix_correlations_2d_1.name = "correlation"
        correlations_2d_1 = pd.pivot_table(
            matrix_correlations_2d_1.to_frame(),
            values="correlation",
            index="dimension_2",
            columns="category",
            dropna=False,
        ).fillna(0)

        matrix_number_variables_2d_1 = correlations["number_variables"].loc[dimension, "number_variables"].swaplevel()
        matrix_number_variables_2d_1.name = "number_variables"
        number_variables_2d_1 = pd.pivot_table(
            matrix_number_variables_2d_1.to_frame(),
            values="number_variables",
            index="dimension_2",
            columns="category",
            dropna=False,
        ).fillna(0)

    if dimension == DIMENSIONS[0]:
        correlations_2d_2 = None
        number_variables_2d_2 = None
    else:
        matrix_correlations_2d_2 = correlations[correlation_type].swaplevel(i=0, j=1).loc[dimension, "mean"]
        matrix_correlations_2d_2.name = "correlation"
        correlations_2d_2 = pd.pivot_table(
            matrix_correlations_2d_2.to_frame(),
            values="correlation",
            index="dimension_1",
            columns="category",
            dropna=False,
        ).fillna(0)

        matrix_number_variables_2d_2 = (
            correlations["number_variables"].swaplevel(i=0, j=1).loc[dimension, "number_variables"]
        )
        matrix_number_variables_2d_2.name = "number_variables"
        number_variables_2d_2 = pd.pivot_table(
            matrix_number_variables_2d_2.to_frame(),
            values="number_variables",
            index="dimension_1",
            columns="category",
            dropna=False,
        ).fillna(0)

    correlations_2d_concat = pd.concat([correlations_2d_1, correlations_2d_2])
    correlations_2d = correlations_2d_concat.loc[
        pd.Index(DIMENSIONS).drop(dimension)
    ]  # remove dimension since upper matrix

    number_variables_2d_concat = pd.concat([number_variables_2d_1, number_variables_2d_2]).astype(int)
    number_variables_2d = number_variables_2d_concat.loc[
        pd.Index(DIMENSIONS).drop(dimension)
    ]  # remove dimension since upper matrix

    hovertemplate = "Correlation: %{z:.3f} <br>X subcategory: %{x} <br>Aging dimension: %{y} <br>Number variables: %{customdata} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=correlations_2d.columns,
        y=correlations_2d.index,
        z=correlations_2d,
        colorscale=get_colorscale(correlations_2d),
        customdata=number_variables_2d,
        hovertemplate=hovertemplate,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        {
            "width": 2000,
            "height": 1000,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "Aging dimension", "showgrid": False},
        }
    )

    return fig, "Average correlation = ??? ± ???"