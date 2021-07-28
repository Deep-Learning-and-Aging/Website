from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items
from dash_website import DOWNLOAD_CONFIG, CUSTOM_DIMENSIONS, RENAME_DIMENSIONS, ALGORITHMS, CORRELATION_TYPES
from dash_website.utils import BLUE_WHITE_RED


def get_dimension_heatmap():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_dimension_multi")),
            html.H1("Multivariate XWAS - Correlations"),
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
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_dimension_multi"),
                                    dcc.Graph(id="graph_dimension_multi", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 9},
                        style={"overflowX": "scroll"},
                    ),
                ]
            ),
        ],
        fluid=True,
    )


@APP.callback(Output("memory_dimension_multi", "data"), Input("dimension_dimension_multi", "value"))
def _modify_store_dimension_multi(dimension):
    return load_feather(
        f"xwas/multivariate_correlations/correlations/dimensions/correlations_{RENAME_DIMENSIONS.get(dimension, dimension)}.feather"
    ).to_dict()


def get_controls_tab_dimension_multi():

    return dbc.Card(
        [
            get_drop_down(
                "dimension_dimension_multi",
                CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates(),
                "Select an aging dimension: ",
                from_dict=False,
            ),
            get_item_radio_items(
                "algorithm_dimension",
                {
                    "elastic_net": ALGORITHMS["elastic_net"],
                    "light_gbm": ALGORITHMS["light_gbm"],
                    "neural_network": ALGORITHMS["neural_network"],
                },
                "Select an Algorithm :",
            ),
            get_item_radio_items("correlation_type_category_multi", CORRELATION_TYPES, "Select correlation type :"),
        ]
    )


@APP.callback(
    [Output("graph_dimension_multi", "figure"), Output("title_dimension_multi", "children")],
    [
        Input("algorithm_dimension", "value"),
        Input("correlation_type_category_multi", "value"),
        Input("memory_dimension_multi", "data"),
    ],
)
def _fill_graph_tab_dimension_multi(algorithm, correlation_type, data_dimension):
    import plotly.graph_objs as go

    correlations_raw = pd.DataFrame(data_dimension).set_index(["dimension", "subdimension", "category"])
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["algorithm", "correlation_type"]
    )
    correlations = correlations_raw[[(algorithm, correlation_type)]]
    correlations.columns = ["correlation"]
    correlations["dimension_subdimension"] = (
        correlations.index.get_level_values("dimension") + " - " + correlations.index.get_level_values("subdimension")
    )
    numbers_features = correlations_raw[[(algorithm, "number_features")]]
    numbers_features.columns = ["number_features"]
    numbers_features["dimension_subdimension"] = (
        numbers_features.index.get_level_values("dimension")
        + " - "
        + numbers_features.index.get_level_values("subdimension")
    )

    correlations_2d = pd.pivot_table(
        correlations, values="correlation", index="dimension_subdimension", columns="category", dropna=False
    ).fillna(0)

    numbers_features_2d = pd.pivot_table(
        numbers_features, values="number_features", index="dimension_subdimension", columns="category", dropna=False
    ).fillna(0)

    hovertemplate = "Correlation: %{z:.3f} <br>X subcategory: %{x} <br>Aging dimension: %{y} <br>Number features: %{customdata} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=correlations_2d.columns,
        y=correlations_2d.index,
        z=correlations_2d,
        colorscale=BLUE_WHITE_RED,
        customdata=numbers_features_2d,
        hovertemplate=hovertemplate,
        zmin=-1,
        zmax=1,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        {
            "width": 2000,
            "height": 1000,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": "Aging dimension", "showgrid": False, "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    return (
        fig,
        f"Average correlation on feature importances = {correlations_2d.values.flatten().mean().round(3)} ± {correlations_2d.values.flatten().std().round(3)}",
    )
