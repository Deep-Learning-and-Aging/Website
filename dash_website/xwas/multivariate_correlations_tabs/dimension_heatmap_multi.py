from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import (
    get_dimension_drop_down,
    get_subset_method_radio_items,
    get_correlation_type_radio_items,
)
from dash_website import DIMENSIONS, RENAME_DIMENSIONS


def get_dimension_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_dimension_multi")),
            html.H1("Multivariate XWAS - Correlations between accelerated aging"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_dimension(),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_dimension_multi"),
                                    dcc.Graph(id="graph_dimension_multi"),
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


@APP.callback(Output("memory_dimension_multi", "data"), Input("dimension_dimension_multi", "value"))
def _modify_store_dimension(dimension):
    return load_feather(
        f"xwas/univariate_correlations/correlations/dimensions/correlations_{dimension}.feather"
    ).to_dict()


def get_controls_tab_dimension():
    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension_multi", DIMENSIONS),
            get_subset_method_radio_items("subset_method_category_multi"),
            get_correlation_type_radio_items("correlation_type_category_multi"),
        ]
    )


@APP.callback(
    [Output("graph_dimension_multi", "figure"), Output("title_dimension_multi", "children")],
    [
        Input("dimension_dimension_multi", "value"),
        Input("subset_method_category_multi", "value"),
        Input("correlation_type_category_multi", "value"),
        Input("memory_dimension_multi", "data"),
    ],
)
def _fill_graph_tab_organ(dimension, subset_method, correlation_type, data_dimension):
    from dash_website.utils.graphs.colorscale import get_colorscale
    import plotly.graph_objs as go

    correlations_raw = pd.DataFrame(data_dimension).set_index(["dimension", "category"])
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations = correlations_raw[[(subset_method, correlation_type)]]
    correlations.columns = ["correlation"]
    numbers_variables = correlations_raw[[(subset_method, "number_variables")]]
    numbers_variables.columns = ["number_variables"]

    correlations_2d = pd.pivot_table(
        correlations, values="correlation", index="dimension", columns="category", dropna=False
    ).fillna(0)
    correlations_2d.drop(index=dimension, inplace=True)
    correlations_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

    numbers_variables_2d = pd.pivot_table(
        numbers_variables, values="number_variables", index="dimension", columns="category", dropna=False
    ).fillna(0)
    numbers_variables_2d.drop(index=dimension, inplace=True)
    numbers_variables_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

    hovertemplate = "Correlation: %{z:.3f} <br>X subcategory: %{x} <br>Aging dimension: %{y} <br>Number variables: %{customdata} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=correlations_2d.columns,
        y=correlations_2d.index,
        z=correlations_2d,
        colorscale=get_colorscale(correlations_2d),
        customdata=numbers_variables_2d,
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
