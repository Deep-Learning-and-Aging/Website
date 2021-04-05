from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import (
    get_main_category_radio_items,
    get_dimension_drop_down,
    get_item_radio_items,
    get_options,
)
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES, LIST_MAIN_CATEGORY_CATEGORIES


def get_average_bars(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Container(
        [
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dcc.Loading([dcc.Store(id="memory_averages", data=get_data())]),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_average(subset_method_radio_items, correlation_type_radio_items),
                            html.Br(),
                            html.Br(),
                        ],
                        md=3,
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_average_test"),
                                    dcc.Graph(id="graph_average"),
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


def get_data():
    return load_feather(f"xwas/univariate_correlations/averages_correlations.feather").to_dict()


def get_controls_tab_average(subset_method_radio_items, correlation_type_radio_items):
    return dbc.Card(
        [
            get_main_category_radio_items("main_category_average", list(MAIN_CATEGORIES_TO_CATEGORIES.keys())),
            get_dimension_drop_down(
                "dimension_1_average", ["MainDimensions", "SubDimensions"] + DIMENSIONS, idx_dimension=1
            ),
            html.Div(
                [get_dimension_drop_down("dimension_2_average", ["average"] + DIMENSIONS, idx_dimension=2)],
                id="hiden_dimension_2_average",
                style={"display": "none"},
            ),
            get_item_radio_items(
                "display_mode_average", {"view_all": "View All", "view_per_main_category": "View per X main category"}
            ),
            subset_method_radio_items,
            correlation_type_radio_items,
        ]
    )


@APP.callback(
    [
        Output("hiden_dimension_2_average", component_property="style"),
        Output("dimension_2_average", "options"),
        Output("dimension_2_average", "value"),
    ],
    Input("dimension_1_average", "value"),
)
def _change_controls_average(dimension_1):
    if dimension_1 in ["MainDimensions", "SubDimensions"]:
        return {"display": "none"}, get_options(["average"]), "average"
    else:
        return (
            {"display": "block"},
            get_options(["average"] + pd.Index(DIMENSIONS).drop(dimension_1).tolist()),
            "average",
        )


@APP.callback(
    [Output("graph_average", "figure"), Output("title_average_test", "children")],
    [
        Input("subset_method_correlations", "value"),
        Input("correlation_type_correlations", "value"),
        Input("main_category_average", "value"),
        Input("dimension_1_average", "value"),
        Input("dimension_2_average", "value"),
        Input("display_mode_average", "value"),
        Input("memory_correlations", "data"),
        Input("memory_averages", "data"),
    ],
)
def _fill_graph_tab_average(
    subset_method,
    correlation_type,
    main_category,
    dimension_1,
    dimension_2,
    display_mode,
    data_correlations,
    data_averages,
):
    import plotly.graph_objs as go

    if dimension_2 == "average":
        averages = pd.DataFrame(data_averages).set_index(["dimension", "category"])
        averages.columns = pd.MultiIndex.from_tuples(
            list(map(eval, averages.columns.tolist())), names=["subset_method", "correlation_type", "observation"]
        )
        sorted_averages = averages.loc[
            (dimension_1, MAIN_CATEGORIES_TO_CATEGORIES[main_category]), (subset_method, correlation_type)
        ].sort_values(by=["mean"], ascending=False)

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_averages.index.get_level_values("category"),
                y=sorted_averages["mean"],
                error_y={"array": sorted_averages["std"], "type": "data"},
                name="Average correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category
            list_main_category = []
            list_categories = []
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_averages.swaplevel()
                    .loc[MAIN_CATEGORIES_TO_CATEGORIES[main_category_group]]
                    .sort_values(by=["mean"], ascending=False)
                    .index.get_level_values("category")
                )
                list_categories.extend(sorted_categories)
                list_main_category.extend([main_category_group] * len(sorted_categories))

                bars = go.Bar(
                    x=[list_main_category + [""], list_categories + ["FamilyHistory"]],
                    y=sorted_averages["mean"].swaplevel()[list_categories + ["FamilyHistory"]],
                    error_y={
                        "array": sorted_averages["std"].swaplevel()[list_categories + ["FamilyHistory"]],
                        "type": "data",
                    },
                    name="Correlations",
                    marker_color="indianred",
                )

        title = f"Average average correlation across aging dimensions and X categories = {sorted_averages['mean'].mean().round(3)} +- {sorted_averages['mean'].std().round(3)}"
        y_label = "Average correlation"

    else:
        correlations = pd.DataFrame(data_correlations).set_index(["dimension_1", "dimension_2", "category"])

        sorted_correlations = correlations.loc[
            (dimension_1, dimension_2, MAIN_CATEGORIES_TO_CATEGORIES[main_category])
        ].sort_values(by=["correlation"], ascending=False)

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_correlations.index.get_level_values("category"),
                y=sorted_correlations["correlation"],
                name="Correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category
            list_main_category = []
            list_categories = []
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_correlations["correlation"]
                    .swaplevel()
                    .swaplevel(i=0, j=1)[MAIN_CATEGORIES_TO_CATEGORIES[main_category_group]]
                    .sort_values(ascending=False)
                    .index.get_level_values("category")
                )
                list_categories.extend(sorted_categories)
                list_main_category.extend([main_category_group] * len(sorted_categories))

            bars = go.Bar(
                x=[list_main_category + [""], list_categories + ["FamilyHistory"]],
                y=sorted_correlations["correlation"]
                .swaplevel()
                .swaplevel(i=0, j=1)[list_categories + ["FamilyHistory"]],
                name="Correlations",
                marker_color="indianred",
            )

        title = f"Average correlation = {sorted_correlations['correlation'].mean().round(3)} +- {sorted_correlations['correlation'].std().round(3)}"
        y_label = "Correlation"

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 2000,
            "height": 800,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False},
            "yaxis": {"title": y_label},
        }
    )

    return fig, title
