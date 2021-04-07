from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np

from dash_website.utils.controls import get_main_category_radio_items, get_drop_down
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
            get_drop_down(
                "algorithm_heatmap",
                ALGORITHMS_RENDERING,
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
    std_2d = pd.pivot(scores, index="category", columns="dimension", values="std")
    sample_size_2d = pd.pivot(scores, index="category", columns="dimension", values="sample_size")
    algorithm_2d = pd.pivot(scores, index="category", columns="dimension", values="algorithm").replace(
        ALGORITHMS_RENDERING
    )
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
            None, columns=["percentage", "max_percentage"], index=list(ALGORITHMS_RENDERING.keys())[1:]
        )
        percentages.index.name = "algorithm"
        for algorithm in list(ALGORITHMS_RENDERING.keys())[1:]:
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
            f"Average r² = {r2_2d.values.flatten().mean().round(3)} +- {r2_2d.values.flatten().std().round(3)}",
            {"display": "block"},
            fig_pie_chart,
        )
    else:
        return (
            fig,
            f"Average r² = {r2_2d.values.flatten().mean().round(3)} +- {r2_2d.values.flatten().std().round(3)}",
            {"display": "none"},
            dash.no_update,
        )
