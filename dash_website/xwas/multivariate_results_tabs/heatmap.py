from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np

from dash_website.utils.controls import get_main_category_radio_items, get_item_radio_items
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS, ALGORITHMS_RENDERING


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
                        [dcc.Loading([html.H2(id="title_heatmap"), dcc.Graph(id="heatmap_heatmap")])],
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
            get_item_radio_items(
                "algorithm_heatmap",
                {
                    "best_algorithm": ALGORITHMS_RENDERING["best_algorithm"],
                    "elastic_net": ALGORITHMS_RENDERING["elastic_net"],
                    "light_gbm": ALGORITHMS_RENDERING["light_gbm"],
                    "neural_network": ALGORITHMS_RENDERING["neural_network"],
                },
                "Select an Algorithm :",
            ),
            html.Div(
                [dcc.Loading(dcc.Graph(id="pie_chart_heatmap"))],
                id="div_pie_chart_heatmap",
                style={"display": "none"},
            ),
        ]
    )


@APP.callback(
    [
        Output("heatmap_heatmap", "figure"),
        Output("title_heatmap", "children"),
        Output("div_pie_chart_heatmap", component_property="style"),
        Output("pie_chart_heatmap", "figure"),
    ],
    [Input("main_category_heatmap", "value"), Input("algorithm_heatmap", "value"), Input("memory_scores", "data")],
)
def _fill_graph_tab_heatmap(main_category, algorithm, data_scores):
    from dash_website.utils.graphs.colorscale import get_colorscale
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

    r2_2d = pd.pivot(scores, index="category", columns="dimension", values="r2").rename(columns=RENAME_DIMENSIONS)
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

    algorithm_2d = pd.pivot(scores, index="category", columns="dimension", values="algorithm").replace(
        ALGORITHMS_RENDERING
    )
    algorithm_2d["average"] = "No algorithm"
    algorithm_2d.loc["average"] = "No algorithm"
    algorithm_2d = algorithm_2d.reindex(index=np.roll(algorithm_2d.index, 1), columns=np.roll(algorithm_2d.columns, 1))

    customdata = np.dstack((std_2d, sample_size_2d, algorithm_2d))

    hovertemplate = "Aging dimension: %{x} <br>X subcategory: %{y} <br>r²: %{z:.3f} <br>Standard deviation: %{customdata[0]:.3f} <br>Sample size: %{customdata[1]} <br>Algorithm: %{customdata[2]} <br><extra></extra>"

    heatmap = go.Heatmap(
        x=r2_2d.columns,
        y=r2_2d.index,
        z=r2_2d,
        colorscale=get_colorscale(r2_2d),
        customdata=customdata,
        hovertemplate=hovertemplate,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        {
            "width": 1000,
            "height": int(1000 * max(1, r2_2d.shape[0] / r2_2d.shape[1])),
            "xaxis": {"title": "Aging dimension", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": "X subcategory", "showgrid": False},
        }
    )

    if algorithm == "best_algorithm":
        percentages = pd.DataFrame(
            None, columns=["percentage", "max_percentage"], index=["elastic_net", "light_gbm", "neural_network"]
        )
        percentages.index.name = "algorithm"
        for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
            percentages.loc[algorithm, "percentage"] = (algorithm_2d == ALGORITHMS_RENDERING[algorithm]).sum().sum()
            percentages.loc[algorithm, "max_percentage"] = r2_2d.values[
                algorithm_2d == ALGORITHMS_RENDERING[algorithm]
            ].max()

        percentages.reset_index(inplace=True)
        percentages.replace(ALGORITHMS_RENDERING, inplace=True)

        hovertemplate = "Algorithm: %{label} <br>Number of best algorithm: %{value} <br>Max percentage: %{customdata:.3f} <br><extra></extra>"

        pie_chart = go.Pie(
            labels=percentages["algorithm"],
            values=percentages["percentage"],
            customdata=percentages["max_percentage"],
            hovertemplate=hovertemplate,
        )

        fig_pie_chart = go.Figure(pie_chart)

        fig_pie_chart.update_layout(title="Composition of the best algorithm")

        fig_pie_chart.update_layout(title="Composition of the best algorithms")

        return (
            fig,
            f"Average r² = {overall_mean.round(3)} +- {overall_std.round(3)}",
            {"display": "block"},
            fig_pie_chart,
        )
    else:
        return (
            fig,
            f"Average r² = {overall_mean.round(3)} +- {overall_std.round(3)}",
            {"display": "none"},
            dash.no_update,
        )
