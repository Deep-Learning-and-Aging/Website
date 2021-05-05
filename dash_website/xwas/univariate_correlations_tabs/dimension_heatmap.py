from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items
from dash_website import DOWNLOAD_CONFIG, DIMENSIONS, RENAME_DIMENSIONS, CORRELATION_TYPES
from dash_website.utils import BLUE_WHITE_RED
from dash_website.xwas import SUBSET_METHODS


def get_dimension_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_dimension")),
            html.H1("Univariate XWAS - Correlations"),
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
                                    html.H2(id="title_dimension"),
                                    dcc.Graph(id="graph_dimension", config=DOWNLOAD_CONFIG),
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


@APP.callback(Output("memory_dimension", "data"), Input("dimension_dimension", "value"))
def _modify_store_dimension(dimension):
    return load_feather(
        f"xwas/univariate_correlations/correlations/dimensions/correlations_{dimension}.feather"
    ).to_dict()


def get_controls_tab_dimension():
    return dbc.Card(
        [
            get_drop_down("dimension_dimension", DIMENSIONS, "Select an aging dimension: ", from_dict=False),
            get_item_radio_items("subset_method_dimension", SUBSET_METHODS, "Select subset method :"),
            get_item_radio_items("correlation_type_dimension", CORRELATION_TYPES, "Select correlation type :"),
        ]
    )


@APP.callback(
    [Output("graph_dimension", "figure"), Output("title_dimension", "children")],
    [
        Input("dimension_dimension", "value"),
        Input("subset_method_dimension", "value"),
        Input("correlation_type_dimension", "value"),
        Input("memory_dimension", "data"),
    ],
)
def _fill_graph_tab_dimension(dimension, subset_method, correlation_type, data_dimension):
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
        colorscale=BLUE_WHITE_RED,
        customdata=numbers_variables_2d,
        hovertemplate=hovertemplate,
        zmin=-1,
        zmax=1,
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
