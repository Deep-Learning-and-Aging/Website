from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np

from dash_website.utils.controls import get_item_radio_items
from dash_website import DIMENSIONS_SUBDIMENSIONS, DOWNLOAD_CONFIG, MAIN_CATEGORIES_TO_CATEGORIES, ALGORITHMS
from dash_website.utils import BLUE_WHITE


def get_heatmap_multivariate_results():
    return dbc.Container(
        [
            html.H1("Accelerated aging prediction performance - XWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab_heatmap_multivariate_results(), html.Br(), html.Br()], width={"size": 3}),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_heatmap_multivariate_results"),
                                    dcc.Graph(id="heatmap_multivariate_results", config=DOWNLOAD_CONFIG),
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


def get_controls_tab_heatmap_multivariate_results():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_heatmap_multivariate_results",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_item_radio_items(
                "algorithm_heatmap_multivariate_results",
                {
                    "best_algorithm": ALGORITHMS["best_algorithm"],
                    "elastic_net": ALGORITHMS["elastic_net"],
                    "light_gbm": ALGORITHMS["light_gbm"],
                    "neural_network": ALGORITHMS["neural_network"],
                },
                "Select an Algorithm :",
            ),
            html.Div(
                [
                    html.H5("Composition of the best algorithm"),
                    dcc.Loading(dcc.Graph(id="pie_chart_heatmap_multivariate_results", config=DOWNLOAD_CONFIG)),
                ],
                id="div_pie_chart_heatmap_multivariate_results",
                style={"display": "none"},
            ),
        ]
    )


@APP.callback(
    [
        Output("heatmap_multivariate_results", "figure"),
        Output("title_heatmap_multivariate_results", "children"),
        Output("div_pie_chart_heatmap_multivariate_results", component_property="style"),
        Output("pie_chart_heatmap_multivariate_results", "figure"),
    ],
    [
        Input("main_category_heatmap_multivariate_results", "value"),
        Input("algorithm_heatmap_multivariate_results", "value"),
        Input("memory_scores_multivariate_results", "data"),
    ],
)
def _fill_graph_tab_heatmap(main_category, algorithm, data_scores):
    import plotly.graph_objs as go

    if algorithm == "best_algorithm":
        every_score = (
            pd.DataFrame(data_scores)
            .groupby(by=["category", "dimension"])
            .apply(
                lambda score_category_dimension: score_category_dimension.iloc[score_category_dimension["r2"].argmax()]
            )
            .reset_index(drop=True)
        )
    else:
        every_score = pd.DataFrame(data_scores).set_index("algorithm").loc[algorithm].reset_index()
    scores = every_score.loc[every_score["category"].isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category])]

    r2_2d = pd.pivot(scores, index="category", columns="dimension", values="r2").rename(columns=DIMENSIONS_SUBDIMENSIONS)
    overall_mean = r2_2d.values.flatten().mean()
    overall_std = r2_2d.values.flatten().std()
    r2_2d["average"] = r2_2d.T.mean()
    r2_2d.loc["average"] = r2_2d.mean()
    r2_2d.loc["average", "average"] = overall_mean
    r2_2d = r2_2d.reindex(index=np.roll(r2_2d.index, 1), columns=np.roll(r2_2d.columns, 1))

    std_2d = pd.pivot(scores, index="category", columns="dimension", values="std")
    std_2d["average"] = r2_2d.T.std()
    std_2d.loc["average"] = r2_2d.std()
    std_2d.loc["average", "average"] = overall_std
    std_2d = std_2d.reindex(index=np.roll(std_2d.index, 1), columns=np.roll(std_2d.columns, 1))

    sample_size_2d = pd.pivot(scores, index="category", columns="dimension", values="sample_size")
    sample_size_2d["average"] = sample_size_2d.T.sum()
    sample_size_2d.loc["average"] = sample_size_2d.sum()
    sample_size_2d = sample_size_2d.reindex(
        index=np.roll(sample_size_2d.index, 1), columns=np.roll(sample_size_2d.columns, 1)
    )

    algorithm_2d = pd.pivot(scores, index="category", columns="dimension", values="algorithm").replace(ALGORITHMS)
    algorithm_2d["average"] = "No algorithm"
    algorithm_2d.loc["average"] = "No algorithm"
    algorithm_2d = algorithm_2d.reindex(index=np.roll(algorithm_2d.index, 1), columns=np.roll(algorithm_2d.columns, 1))

    customdata = np.dstack((std_2d, sample_size_2d, algorithm_2d))

    hovertemplate = "Aging dimension: %{x} <br>X subcategory: %{y} <br>R²: %{z:.3f} +- %{customdata[0]:.3f} <br>Sample size: %{customdata[1]} <br>Algorithm: %{customdata[2]} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=r2_2d.columns,
        y=r2_2d.index,
        z=r2_2d,
        colorscale=BLUE_WHITE,
        customdata=customdata,
        hovertemplate=hovertemplate,
        zmax=1,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        {
            "width": 1000,
            "height": int(1000 * max(1, r2_2d.shape[0] / r2_2d.shape[1])),
            "xaxis": {"title": "Aging dimension", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": "X subcategory", "showgrid": False, "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    if algorithm == "best_algorithm":
        percentages = pd.DataFrame(
            None, columns=["percentage", "max_percentage"], index=["elastic_net", "light_gbm", "neural_network"]
        )
        percentages.index.name = "algorithm"
        for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
            percentages.loc[algorithm, "percentage"] = (algorithm_2d == ALGORITHMS[algorithm]).sum().sum()
            percentages.loc[algorithm, "max_percentage"] = r2_2d.values[algorithm_2d == ALGORITHMS[algorithm]].max()

        percentages.reset_index(inplace=True)
        percentages.replace(ALGORITHMS, inplace=True)

        hovertemplate = "Algorithm: %{label} <br>Number of best algorithm: %{value} <br>Max percentage: %{customdata:.3f} <br><extra></extra>"

        pie_chart = go.Pie(
            labels=percentages["algorithm"],
            values=percentages["percentage"],
            customdata=percentages["max_percentage"],
            hovertemplate=hovertemplate,
        )

        fig_pie_chart = go.Figure(pie_chart)

        fig_pie_chart.update_layout(
            margin={"l": 0, "r": 0, "b": 0, "t": 0},
        )

        return (
            fig,
            f"Average R² = {overall_mean.round(3)} +- {overall_std.round(3)}",
            {"display": "block"},
            fig_pie_chart,
        )
    else:
        return (
            fig,
            f"Average R² = {overall_mean.round(3)} +- {overall_std.round(3)}",
            {"display": "none"},
            dash.no_update,
        )
