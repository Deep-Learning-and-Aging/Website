from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plotly.graph_objs import Figure

from dash_website.utils.controls import get_main_category_radio_items, get_drop_down
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES


def get_heatmap():
    return dbc.Container(
        [
            html.H1("Multivariate XWAS - Results"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab_heatmap(), html.Br(), html.Br()], md=3),
                    dbc.Col(
                        [dcc.Loading(dcc.Graph(id="heatmap_heatmap"))],
                        style={"overflowX": "scroll", "width": 1000},
                        md=9,
                    ),
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_tab_heatmap():
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_heatmap", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_drop_down(
                "algorithm_heatmap",
                {
                    "elastic_net": "ElasticNet",
                    "light_gbm": "LightGbm",
                    "neural_network": "NeuralNetwork",
                    "best_algorithm": "Best Algorithm",
                },
                "Select an Algorithm :",
            ),
        ]
    )


@APP.callback(
    Output("heatmap_heatmap", "figure"),
    [Input("main_category_heatmap", "value"), Input("algorithm_heatmap", "value")],
)
def _fill_graph_tab_heatmap(main_category, algorithm):
    return Figure()
