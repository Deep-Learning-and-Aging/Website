from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import (
    get_dimension_drop_down,
    get_item_radio_items,
    get_correlation_type_radio_items,
)
from dash_website import DIMENSIONS, RENAME_DIMENSIONS, ALGORITHMS_RENDERING


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
                            get_controls_tab_dimension_multi(),
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
def _modify_store_dimension_multi(dimension):
    return load_feather(
        f"xwas/multivariate_correlations/correlations/dimensions/correlations_{dimension}.feather"
    ).to_dict()


def get_controls_tab_dimension_multi():
    if "best_algorithm" in ALGORITHMS_RENDERING.keys():
        ALGORITHMS_RENDERING.pop("best_algorithm")

    return dbc.Card(
        [
            get_dimension_drop_down("dimension_dimension_multi", DIMENSIONS),
            get_item_radio_items(
                "algorithm_dimension",
                ALGORITHMS_RENDERING,
                "Select an Algorithm :",
            ),
            get_correlation_type_radio_items("correlation_type_category_multi"),
        ]
    )


@APP.callback(
    [Output("graph_dimension_multi", "figure"), Output("title_dimension_multi", "children")],
    [
        Input("dimension_dimension_multi", "value"),
        Input("algorithm_dimension", "value"),
        Input("correlation_type_category_multi", "value"),
        Input("memory_dimension_multi", "data"),
    ],
)
def _fill_graph_tab_dimension_multi(dimension, algorithm, correlation_type, data_dimension):
    from dash_website.utils.graphs.colorscale import get_colorscale
    import plotly.graph_objs as go

    correlations_raw = pd.DataFrame(data_dimension).set_index(["dimension", "category"])
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["algorithm", "correlation_type"]
    )
    correlations = correlations_raw[[(algorithm, correlation_type)]]
    correlations.columns = ["correlation"]
    numbers_features = correlations_raw[[(algorithm, "number_features")]]
    numbers_features.columns = ["number_features"]

    correlations_2d = pd.pivot_table(
        correlations, values="correlation", index="dimension", columns="category", dropna=False
    ).fillna(0)
    correlations_2d.drop(index=dimension, inplace=True)
    correlations_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

    numbers_features_2d = pd.pivot_table(
        numbers_features, values="number_features", index="dimension", columns="category", dropna=False
    ).fillna(0)
    numbers_features_2d.drop(index=dimension, inplace=True)
    numbers_features_2d.rename(index=RENAME_DIMENSIONS, inplace=True)

    hovertemplate = "Correlation: %{z:.3f} <br>X subcategory: %{x} <br>Aging dimension: %{y} <br>Number features: %{customdata} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=correlations_2d.columns,
        y=correlations_2d.index,
        z=correlations_2d,
        colorscale=get_colorscale(correlations_2d),
        customdata=numbers_features_2d,
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
        f"Average correlation on feature importances = {correlations_2d.values.flatten().mean().round(3)} ± {correlations_2d.values.flatten().std().round(3)}",
    )
