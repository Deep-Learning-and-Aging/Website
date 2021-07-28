from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down, get_item_radio_items, get_options_from_list
from dash_website import (
    DOWNLOAD_CONFIG,
    CUSTOM_DIMENSIONS,
    MAIN_CATEGORIES_TO_CATEGORIES,
    CORRELATION_TYPES,
    RENAME_DIMENSIONS,
)
from dash_website.xwas import SUBSET_METHODS, DISPLAY_MODE


def get_average_bars():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_average", data=get_data()), dcc.Store(id="memory_correlations")]),
            html.H1("Univariate XWAS - Correlations"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_tab_average(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2(id="title_average_test"),
                                    dcc.Graph(id="graph_average", config=DOWNLOAD_CONFIG),
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


def get_data():
    return load_feather(f"xwas/univariate_correlations/averages_correlations.feather").to_dict()


@APP.callback(
    Output("memory_correlations", "data"),
    [Input("dimension_1_average", "value"), Input("dimension_2_average", "value")],
)
def _modify_store_correlations(dimension_1, dimension_2):
    if dimension_2 == "average":
        raise PreventUpdate
    else:
        return load_feather(
            f"xwas/univariate_correlations/correlations/dimensions/correlations_{RENAME_DIMENSIONS.get(dimension_1, dimension_1)}.feather"
        ).to_dict()


def get_controls_tab_average():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_average",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_drop_down(
                "dimension_1_average",
                ["MainDimensions", "SubDimensions"]
                + CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates().to_list(),
                "Select an aging dimension 1: ",
                from_dict=False,
            ),
            html.Div(
                [
                    get_drop_down(
                        "dimension_2_average",
                        ["average"] + CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates().to_list(),
                        "Select an aging dimension 2: ",
                        from_dict=False,
                    )
                ],
                id="hiden_dimension_2_average",
                style={"display": "none"},
            ),
            get_item_radio_items(
                "display_mode_average",
                DISPLAY_MODE,
                "Rank by : ",
            ),
            get_item_radio_items("subset_method_average", SUBSET_METHODS, "Select subset method :"),
            get_item_radio_items("correlation_type_average", CORRELATION_TYPES, "Select correlation type :"),
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
        return {"display": "none"}, get_options_from_list(["average"]), "average"
    else:
        return (
            {"display": "block"},
            get_options_from_list(
                ["average"]
                + CUSTOM_DIMENSIONS.get_level_values("dimension").drop_duplicates().drop(dimension_1).tolist()
            ),
            "average",
        )


@APP.callback(
    [Output("graph_average", "figure"), Output("title_average_test", "children")],
    [
        Input("subset_method_average", "value"),
        Input("correlation_type_average", "value"),
        Input("main_category_average", "value"),
        Input("dimension_1_average", "value"),
        Input("dimension_2_average", "value"),
        Input("display_mode_average", "value"),
        Input("memory_correlations", "data"),
        Input("memory_average", "data"),
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

    if main_category == "All":
        all_main_categories = [f"All_{main_cat}" for main_cat in MAIN_CATEGORIES_TO_CATEGORIES.keys()]
    else:
        all_main_categories = [f"All_{main_category}"]

    if dimension_2 == "average":
        averages = pd.DataFrame(data_averages).set_index(["dimension", "category"])
        averages.columns = pd.MultiIndex.from_tuples(
            list(map(eval, averages.columns.tolist())), names=["subset_method", "correlation_type", "observation"]
        )

        sorted_averages = averages.loc[
            (dimension_1, MAIN_CATEGORIES_TO_CATEGORIES[main_category] + all_main_categories),
            (subset_method, correlation_type),
        ].sort_values(by=["mean"], ascending=False)

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_averages.index.get_level_values("category"),
                y=sorted_averages["mean"],
                error_y={"array": sorted_averages["std"], "type": "data"},
                name="Average correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category then main_category = All
            list_main_category = []
            list_categories = []
            # Get the ranking of subcategories per main category
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_averages.swaplevel()
                    .loc[MAIN_CATEGORIES_TO_CATEGORIES[main_category_group] + [f"All_{main_category_group}"]]
                    .sort_values(by=["mean"], ascending=False)
                )
                sorted_index_categories = sorted_categories.index.get_level_values("category")

                list_categories.extend(sorted_index_categories)
                list_main_category.extend([main_category_group] * len(sorted_index_categories))

            bars = go.Bar(
                x=[list_main_category + ["", "", ""], list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
                y=sorted_averages["mean"].swaplevel()[list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
                error_y={
                    "array": sorted_averages["std"].swaplevel()[
                        list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]
                    ],
                    "type": "data",
                },
                name="Correlations",
                marker_color="indianred",
            )

        title = f"Average average correlation across aging dimensions and X categories = {sorted_averages['mean'].mean().round(3)} +- {sorted_averages['mean'].std().round(3)}"
        y_label = "Average correlation"
    else:
        correlations_raw = pd.DataFrame(data_correlations).set_index(["dimension", "subdimension", "category"])
        correlations_raw.columns = pd.MultiIndex.from_tuples(
            list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
        )
        correlations_raw.reset_index(inplace=True)
        correlations_raw["squeezed_dimension"] = correlations_raw["dimension"] + correlations_raw[
            "subdimension"
        ].replace("*", "")
        correlations_raw = correlations_raw.drop(columns=["dimension", "subdimension"]).set_index(
            ["squeezed_dimension", "category"]
        )

        sorted_correlations = correlations_raw.loc[
            (dimension_2, MAIN_CATEGORIES_TO_CATEGORIES[main_category] + all_main_categories),
            (subset_method, correlation_type),
        ].sort_values(ascending=False)

        if display_mode == "view_all":
            bars = go.Bar(
                x=sorted_correlations.index.get_level_values("category"),
                y=sorted_correlations,
                name="Correlations",
                marker_color="indianred",
            )
        else:  # display_mode == view_per_main_category
            list_main_category = []
            list_categories = []
            # Get the ranking of subcategories per main category
            for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
                if main_category_group == "All":
                    continue
                sorted_categories = (
                    sorted_correlations.swaplevel()
                    .loc[MAIN_CATEGORIES_TO_CATEGORIES[main_category_group] + [f"All_{main_category_group}"]]
                    .sort_values(ascending=False)
                )
                sorted_index_categories = sorted_categories.index.get_level_values("category")

                list_categories.extend(sorted_index_categories)
                list_main_category.extend([main_category_group] * len(sorted_index_categories))

            bars = go.Bar(
                x=[list_main_category + ["", "", ""], list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
                y=sorted_correlations.swaplevel()[list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
                name="Correlations",
                marker_color="indianred",
            )

        title = f"Average correlation = {sorted_correlations.mean().round(3)} +- {sorted_correlations.std().round(3)}"
        y_label = "Correlation"

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 2000,
            "height": 800,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": y_label, "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 280, "t": 0},
        }
    )

    return fig, title
