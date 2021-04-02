from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import get_dimension_drop_down
from dash_website import DIMENSIONS, RENAME_DIMENSIONS


def get_dimension_heatmap(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_dimension(subset_method_radio_items, correlation_type_radio_items),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_dimension"),
                                    dcc.Graph(id="graph_dimension"),
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


def get_controls_tab_dimension(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension", DIMENSIONS),
            subset_method_radio_items,
            correlation_type_radio_items,
        ]
    )


@APP.callback(
    [Output("graph_dimension", "figure"), Output("title_dimension", "children")],
    [
        Input("dimension_dimension", "value"),
        Input("memory_correlations", "data"),
        Input("memory_number_variables", "data"),
    ],
)
def _fill_graph_tab_organ(dimension, data_correlations, data_number_variables):
    from dash_website.utils.graphs.colorscale import get_colorscale
    import plotly.graph_objs as go

    correlations = pd.DataFrame(data_correlations).set_index(["dimension_1", "dimension_2", "category"])
    number_variables = pd.DataFrame(data_number_variables).set_index(["dimension_1", "dimension_2", "category"])

    correlations_2d = pd.pivot_table(
        correlations.loc[dimension], values="correlation", index="dimension_2", columns="category", dropna=False
    ).fillna(0)
    correlations_2d.drop(index=dimension, inplace=True)
    correlations_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

    number_variables_2d = pd.pivot_table(
        number_variables.loc[dimension],
        values="number_variables",
        index="dimension_2",
        columns="category",
        dropna=False,
    ).fillna(0)
    number_variables_2d.drop(index=dimension, inplace=True)
    number_variables_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

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

    return (
        fig,
        f"Average correlation = {correlations_2d.values.flatten().mean().round(3)} ± {correlations_2d.values.flatten().std().round(3)}",
    )
