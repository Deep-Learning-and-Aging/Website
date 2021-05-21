from re import A

from botocore.exceptions import AliasConflictParameterError
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import get_drop_down, get_item_radio_items
from dash_website import DOWNLOAD_CONFIG, MAIN_CATEGORIES_TO_CATEGORIES, DIMENSIONS, ALGORITHMS_RENDERING, GRAPH_SIZE


def get_bar_plot():
    return dbc.Container(
        [
            html.H1("Accelerated aging prediction performance - XWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab_bar_plot(), html.Br(), html.Br()], width={"size": 3}),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_bar_plot"),
                                    dcc.Graph(id="bar_plot_bar_plot", config=DOWNLOAD_CONFIG),
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


def get_controls_tab_bar_plot():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_bar_plot",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down(
                "dimension_bar_plot",
                DIMENSIONS,
                "Select an aging dimension : ",
                from_dict=False,
            ),
            get_item_radio_items(
                "algorithm_bar_plot",
                {
                    "best_algorithm": ALGORITHMS_RENDERING["best_algorithm"],
                    "elastic_net": ALGORITHMS_RENDERING["elastic_net"],
                    "light_gbm": ALGORITHMS_RENDERING["light_gbm"],
                    "neural_network": ALGORITHMS_RENDERING["neural_network"],
                },
                "Select an Algorithm :",
            ),
        ]
    )


@APP.callback(
    [Output("bar_plot_bar_plot", "figure"), Output("title_bar_plot", "children")],
    [
        Input("main_category_bar_plot", "value"),
        Input("dimension_bar_plot", "value"),
        Input("algorithm_bar_plot", "value"),
        Input("memory_scores", "data"),
    ],
)
def _fill_graph_tab_bar_plot(main_category, dimension, algorithm, data_scores):
    import plotly.graph_objs as go

    if algorithm == "best_algorithm":
        every_score_every_dimension = (
            pd.DataFrame(data_scores)
            .groupby(by=["category", "dimension"])
            .apply(
                lambda score_category_dimension: score_category_dimension.iloc[score_category_dimension["r2"].argmax()]
            )
            .reset_index(drop=True)
        )
        every_score = every_score_every_dimension.set_index("dimension").loc[dimension].reset_index()
    else:
        every_score = (
            pd.DataFrame(data_scores).set_index(["algorithm", "dimension"]).loc[(algorithm, dimension)].reset_index()
        )

    scores = every_score.loc[every_score["category"].isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])].sort_values(
        by=["r2"], ascending=False
    )

    hovertemplate = "X subcategory: %{x} <br>R²: %{y:.3f} +- %{customdata[0]:.3f} <br><extra>%{customdata[1]}</extra>"

    bars = go.Bar(
        x=scores["category"],
        y=scores["r2"],
        error_y={
            "array": scores["std"],
            "type": "data",
        },
        name="Correlations",
        marker_color="indianred",
        hovertemplate=hovertemplate,
        customdata=scores[["std", "algorithm"]],
    )

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": GRAPH_SIZE,
            "height": 800,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": "r2", "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    return fig, f"Average R² = {scores['r2'].mean().round(3)} +- {scores['r2'].std().round(3)}"
