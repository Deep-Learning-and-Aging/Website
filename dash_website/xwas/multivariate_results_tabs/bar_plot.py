from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.controls import get_drop_down, get_item_radio_items
from dash_website import DIMENSIONS_SUBDIMENSIONS, DOWNLOAD_CONFIG, MAIN_CATEGORIES_TO_CATEGORIES, ALGORITHMS, SCORES
from dash_website.xwas import MULTIVARIATE_CATEGORIES_TO_REMOVE
from dash_website.xwas.multivariate_results_tabs import DISPLAY_MODE


def get_bar_plot_multivariate_results():
    return dbc.Container(
        [
            html.H1("Accelerated aging prediction performance - XWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [get_controls_tab_bar_plot_multivariate_results(), html.Br(), html.Br()], width={"size": 3}
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_bar_plot_multivariate_results"),
                                    dcc.Graph(id="bar_plot_bar_plot_multivariate_results", config=DOWNLOAD_CONFIG),
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


def get_controls_tab_bar_plot_multivariate_results():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_bar_plot_multivariate_results",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down(
                "dimension_bar_plot_multivariate_results",
                DIMENSIONS_SUBDIMENSIONS,
                "Select an aging dimension : ",
            ),
            get_item_radio_items(
                "display_mode_bar_plot_multivariate_results",
                DISPLAY_MODE,
                "Rank by : ",
            ),
            get_item_radio_items(
                "algorithm_bar_plot_multivariate_results",
                {
                    "best_algorithm": ALGORITHMS["best_algorithm"],
                    "elastic_net": ALGORITHMS["elastic_net"],
                    "light_gbm": ALGORITHMS["light_gbm"],
                    "neural_network": ALGORITHMS["neural_network"],
                },
                "Select an Algorithm :",
            ),
        ]
    )


@APP.callback(
    [
        Output("bar_plot_bar_plot_multivariate_results", "figure"),
        Output("title_bar_plot_multivariate_results", "children"),
    ],
    [
        Input("main_category_bar_plot_multivariate_results", "value"),
        Input("dimension_bar_plot_multivariate_results", "value"),
        Input("algorithm_bar_plot_multivariate_results", "value"),
        Input("display_mode_bar_plot_multivariate_results", "value"),
        Input("memory_scores_multivariate_results", "data"),
    ],
)
def _fill_graph_tab_bar_plot(main_category, dimension, algorithm, display_mode, data_scores):
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
        every_score = every_score_every_dimension.set_index("dimension").loc[dimension].set_index("category")
    else:
        every_score = (
            pd.DataFrame(data_scores)
            .set_index(["algorithm", "dimension"])
            .loc[(algorithm, dimension)]
            .reset_index()
            .set_index("category")
        )

    multivariate_categories = MAIN_CATEGORIES_TO_CATEGORIES[main_category]
    for to_remove in MULTIVARIATE_CATEGORIES_TO_REMOVE:
        if to_remove in multivariate_categories:
            multivariate_categories.remove(to_remove)

    scores = every_score.loc[multivariate_categories].sort_values(by=["r2"], ascending=False)

    hovertemplate = "X subcategory: %{x} <br>R²: %{y:.3f} +- %{customdata[0]:.3f} <br><extra>%{customdata[1]}</extra>"

    if display_mode == "view_decreasing":
        bars = go.Bar(
            x=scores.index,
            y=scores["r2"],
            error_y={"array": scores["std"], "type": "data"},
            name=SCORES["r2"],
            marker_color="indianred",
            hovertemplate=hovertemplate,
            customdata=scores[["std", "algorithm"]],
        )
    else:  # display_mode == view_per_main_category
        list_main_category = []
        list_categories = []
        # Get the ranking of subcategories per main category
        for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
            if main_category_group == "All":
                continue
            sorted_index_categories = (
                scores.loc[
                    scores.index.isin(
                        MAIN_CATEGORIES_TO_CATEGORIES[main_category_group] + [f"All_{main_category_group}"]
                    )
                ].sort_values(by=["r2"], ascending=False)
            ).index

            list_categories.extend(sorted_index_categories)
            list_main_category.extend([main_category_group] * len(sorted_index_categories))

        if main_category == "All":
            list_categories += ["FamilyHistory"]
            list_main_category += [""]

        bars = go.Bar(
            x=[list_main_category, list_categories],
            y=scores.loc[list_categories, "r2"],
            error_y={"array": scores["std"], "type": "data"},
            name=SCORES["r2"],
            marker_color="indianred",
            hovertemplate=hovertemplate,
            customdata=scores.loc[list_categories, ["std", "algorithm"]],
        )

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "height": 800,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": SCORES["r2"], "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    return fig, f"Average {SCORES['r2']} = {scores['r2'].mean().round(3)} +- {scores['r2'].std().round(3)}"
