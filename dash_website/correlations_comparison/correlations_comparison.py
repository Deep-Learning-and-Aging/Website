from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
from scipy import stats

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_options_from_dict
from dash_website.utils.graphs import heatmap_by_sorted_dimensions, add_custom_legend_axis
from dash_website import (
    DOWNLOAD_CONFIG,
    CORRELATION_TYPES,
    MAIN_CATEGORIES_TO_CATEGORIES,
    ORDER_DIMENSIONS,
    CUSTOM_ORDER,
    ALGORITHMS_RENDERING,
    GRAPH_SIZE,
)
from dash_website.xwas import SUBSET_METHODS, UNIVARIATE_OR_MULTIVARIATE


@APP.callback(
    Output("memory_comparison_upper", "data"),
    [Input("first_uni_or_multi_comparison", "value"), Input("first_category_comparison", "value")],
)
def _modify_store_upper_comparison(uni_or_multi, category):
    return load_feather(
        f"xwas/{uni_or_multi}_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


@APP.callback(
    Output("memory_comparison_lower", "data"),
    [Input("second_uni_or_multi_comparison", "value"), Input("second_category_comparison", "value")],
)
def _modify_store_lower_comparison(uni_or_multi, category):
    return load_feather(
        f"xwas/{uni_or_multi}_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


def get_controls_comparison(order, default_category):
    return dbc.Card(
        [
            get_drop_down(
                f"{order}_category_comparison",
                MAIN_CATEGORIES_TO_CATEGORIES["All"]
                + [f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()],
                f"Select {order} category to compare: ",
                from_dict=False,
                value=default_category,
            ),
            html.Div(
                [
                    get_item_radio_items(
                        f"{order}_uni_or_multi_comparison", UNIVARIATE_OR_MULTIVARIATE, "Select the type of XWAS :"
                    ),
                    get_item_radio_items(f"{order}_method_comparison", SUBSET_METHODS, "Select method :"),
                    get_item_radio_items(
                        f"{order}_correlation_type_comparison", CORRELATION_TYPES, "Select correlation type :"
                    ),
                ],
                id=f"{order}_hiden_settings",
                style={"display": "none"},
            ),
        ]
    )


@APP.callback(
    [
        Output("first_hiden_settings", component_property="style"),
        Output("first_uni_or_multi_comparison", "options"),
        Output("first_uni_or_multi_comparison", "value"),
    ],
    Input("first_category_comparison", "value"),
)
def _change_controls_first_hidden_settings(first_category):
    return display_settings(first_category)


@APP.callback(
    [
        Output("second_hiden_settings", component_property="style"),
        Output("second_uni_or_multi_comparison", "options"),
        Output("second_uni_or_multi_comparison", "value"),
    ],
    Input("second_category_comparison", "value"),
)
def _change_controls_second_hidden_settings(second_category):
    return display_settings(second_category)


def display_settings(category):
    if category in ["Genetics", "Phenotypic"]:
        return {"display": "none"}, get_options_from_dict(UNIVARIATE_OR_MULTIVARIATE), "univariate"
    elif "All" in category:
        return {"display": "block"}, get_options_from_dict({"univariate": "Univariate"}), "univariate"
    else:
        return {"display": "block"}, get_options_from_dict(UNIVARIATE_OR_MULTIVARIATE), "univariate"


@APP.callback(
    [
        Output("first_method_comparison", "options"),
        Output("first_method_comparison", "value"),
    ],
    [Input("first_uni_or_multi_comparison", "value"), Input("first_category_comparison", "value")],
)
def _change_controls_first_method(first_uni_or_multi, first_category):
    return change_method(first_uni_or_multi, first_category)


@APP.callback(
    [
        Output("second_method_comparison", "options"),
        Output("second_method_comparison", "value"),
    ],
    [Input("second_uni_or_multi_comparison", "value"), Input("second_category_comparison", "value")],
)
def _change_controls_second_method(second_uni_or_multi, second_category):
    return change_method(second_uni_or_multi, second_category)


def change_method(uni_or_mutli, category):
    if uni_or_mutli == "univariate" or category in ["Genetics", "Phenotypic"]:
        return get_options_from_dict(SUBSET_METHODS), "union"
    else:  # uni_or_multi == "multivariate"
        return (
            get_options_from_dict(
                {
                    "elastic_net": ALGORITHMS_RENDERING["elastic_net"],
                    "light_gbm": ALGORITHMS_RENDERING["light_gbm"],
                    "neural_network": ALGORITHMS_RENDERING["neural_network"],
                }
            ),
            "elastic_net",
        )


@APP.callback(
    [
        Output("scatter_comparison", "figure"),
        Output("title_comparison", "children"),
        Output("triangular_heatmap_comparison", "figure"),
        Output("title_triangular_heatmap_comparison", "children"),
        Output("difference_heatmap_comparison", "figure"),
        Output("title_difference_heatmap_comparison", "children"),
    ],
    [
        Input("first_uni_or_multi_comparison", "value"),
        Input("first_method_comparison", "value"),
        Input("first_correlation_type_comparison", "value"),
        Input("first_category_comparison", "value"),
        Input("second_uni_or_multi_comparison", "value"),
        Input("second_method_comparison", "value"),
        Input("second_correlation_type_comparison", "value"),
        Input("second_category_comparison", "value"),
        Input("memory_comparison_upper", "data"),
        Input("memory_comparison_lower", "data"),
    ],
)
def _fill_graph_tab_comparison(
    first_uni_or_multi,
    first_method,
    first_correlation_type,
    first_category,
    second_uni_or_multi,
    second_method,
    second_correlation_type,
    second_category,
    data_comparison_upper,
    data_comparison_lower,
):
    import plotly.graph_objs as go

    table_correlations_upper, customdata_upper, correlations_upper = get_table_and_customdata(
        first_uni_or_multi, data_comparison_upper, first_method, first_correlation_type
    )
    np.fill_diagonal(table_correlations_upper.values, np.nan)

    table_correlations_lower, customdata_lower, correlations_lower = get_table_and_customdata(
        second_uni_or_multi, data_comparison_lower, second_method, second_correlation_type
    )
    np.fill_diagonal(table_correlations_lower.values, np.nan)

    fig_points = go.Figure()

    hovertemplate_points = "Dimension 1: %{customdata[0]}, Subdimension 1: %{customdata[1]}<br>Dimenions 2: %{customdata[2]}, Subdimension 2: %{customdata[3]}<Br>Correlation first category %{x:.3f}, Correlation second category %{y:.3f}<extra></extra>"

    y_points = correlations_lower.set_index(["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"])[
        "correlation"
    ]
    y_points[
        (y_points.index.get_level_values("dimension_1") == y_points.index.get_level_values("dimension_2"))
        & (y_points.index.get_level_values("subdimension_1") == y_points.index.get_level_values("subdimension_2"))
    ] = np.nan

    x_points = correlations_upper.set_index(["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"]).loc[
        y_points.index, "correlation"
    ]
    x_points[
        (x_points.index.get_level_values("dimension_1") == x_points.index.get_level_values("dimension_2"))
        & (x_points.index.get_level_values("subdimension_1") == x_points.index.get_level_values("subdimension_2"))
    ] = np.nan

    customdata_points = list(map(list, y_points.index.values))

    fig_points = go.Figure()
    fig_points.add_scatter(x=[-1.1, 1.1], y=[-1.1, 1.1], mode="lines", name="perfect correlation line")

    fig_points.add_scatter(
        x=x_points.values,
        y=y_points.values,
        mode="markers",
        customdata=customdata_points,
        hovertemplate=hovertemplate_points,
        marker={"size": 5},
        name=f"{first_category} vs. {second_category} correlation for one aging dimension",
    )
    correlation_of_correlations, p_value_of_correlations = stats.pearsonr(
        x_points[x_points.notna() & y_points.notna()], y_points[x_points.notna() & y_points.notna()]
    )

    fig_points.update_layout(
        yaxis={
            "title": f"{second_category} correlation",
            "range": [-1.1, 1.1],
            "showgrid": False,
            "title_font": {"size": 25},
        },
        xaxis={
            "title": f"{first_category} correlation",
            "range": [-1.1, 1.1],
            "showgrid": False,
            "title_font": {"size": 25},
        },
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    sorted_dimensions = (
        correlations_upper.set_index(["dimension_1", "subdimension_1"]).loc[CUSTOM_ORDER].index.drop_duplicates()
    )
    if first_category in ["Genetics", "Phenotypic"] and second_category in ["Genetics", "Phenotypic"]:
        sorted_dimensions = sorted_dimensions.drop(("Eyes", "All"))

    sorted_table_correlations_upper = table_correlations_upper.loc[sorted_dimensions, sorted_dimensions]
    sorted_table_correlations_lower = table_correlations_lower.loc[sorted_dimensions, sorted_dimensions]
    sorted_customdata_upper = customdata_upper.loc[sorted_dimensions, sorted_dimensions]
    sorted_customdata_lower = customdata_lower.loc[sorted_dimensions, sorted_dimensions]

    triangular_heatmap_values = np.triu(sorted_table_correlations_upper)
    triangular_heatmap_values += np.tril(sorted_table_correlations_lower, k=-1)
    triangular_heatmap = pd.DataFrame(
        triangular_heatmap_values,
        index=sorted_table_correlations_upper.index,
        columns=sorted_table_correlations_upper.columns,
    )

    customdata_triangular_values = np.triu(sorted_customdata_upper)
    customdata_triangular_values += np.tril(sorted_customdata_lower, k=-1)
    customdata_triangular = pd.DataFrame(
        customdata_triangular_values, index=sorted_customdata_upper.index, columns=sorted_customdata_upper.columns
    )

    hovertemplate_triangular = "Correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[2]:.3f} +- %{customdata[3]:.3f} <br>Number variables: %{customdata[4]}<br><extra></extra>"

    fig_triangular = heatmap_by_sorted_dimensions(triangular_heatmap, hovertemplate_triangular, customdata_triangular)
    fig_triangular = add_custom_legend_axis(fig_triangular, triangular_heatmap)
    fig_triangular.update_layout(
        yaxis={
            "title": f"{second_category} correlation",
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 25},
        },
        xaxis={
            "title": f"{first_category} correlation",
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 25},
        },
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    difference_heatmap = sorted_table_correlations_upper - sorted_table_correlations_lower

    hovertemplate_difference = "Difference in correlation: %{z:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[0]:.3f} +- %{customdata[1]:.3f} <br>Dimensions 2: %{y}<br>R²: %{customdata[2]:.3f} +- %{customdata[3]:.3f}<br><extra></extra>"

    fig_difference = heatmap_by_sorted_dimensions(
        difference_heatmap, hovertemplate_difference, sorted_customdata_upper, zmin=-2, zmax=2
    )
    fig_difference = add_custom_legend_axis(fig_difference, difference_heatmap)
    fig_difference.update_layout(
        yaxis={"showgrid": False, "zeroline": False},
        xaxis={"showgrid": False, "zeroline": False},
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return (
        fig_points,
        f"The correlation between {first_category} and {second_category} is {correlation_of_correlations.round(3)} with the p-value of {format(p_value_of_correlations, '.3e')}",
        fig_triangular,
        f"Heatmap with the bottom right triangle showing the correlations for {first_category} and the top left triangle showing the correlations for {second_category}",
        fig_difference,
        f"Heatmap showing the difference between the correlations from {first_category} and {second_category}",
    )


def get_table_and_customdata(uni_or_multi, data_comparison, method, correlation_type):
    if uni_or_multi == "univariate":
        sample_nature = "number_variables"
    else:  # uni_or_multi == "multivariate"
        sample_nature = "number_features"
    correlations_raw = pd.DataFrame(data_comparison).set_index(
        ["dimension_1", "subdimension_1", "r2_1", "r2_std_1", "dimension_2", "subdimension_2", "r2_2", "r2_std_2"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["method", "correlation_type"]
    )
    correlations = correlations_raw[[(method, correlation_type), (method, sample_nature)]]
    correlations.columns = ["correlation", sample_nature]
    correlations.reset_index(inplace=True)

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]

    customdata_list = []
    for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", sample_nature]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1"],
                columns=["dimension_2", "subdimension_2"],
                values=customdata_item,
            )
            .loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]
            .values
        )

    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(np.nan, index=ORDER_DIMENSIONS, columns=ORDER_DIMENSIONS)
    customdata[customdata.columns] = stacked_customdata

    # Need to get rid of the Nones to be abble to perform addition elementwise
    return table_correlations, customdata.applymap(filter_none_to_nan), correlations


def filter_none_to_nan(customdata_element):
    if customdata_element[-1] is None:
        return np.array(list(customdata_element[:-1]) + [np.nan])
    else:
        return customdata_element


LAYOUT = dbc.Container(
    [
        dcc.Loading(dcc.Store(id="memory_comparison_upper")),
        dcc.Loading(dcc.Store(id="memory_comparison_lower")),
        html.H1("Correlations comparison"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        get_controls_comparison("first", "Genetics"),
                        html.Br(),
                        get_controls_comparison("second", "Phenotypic"),
                        html.Br(),
                        html.Br(),
                    ],
                    width={"size": 3},
                ),
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H2(id="title_comparison"),
                                dcc.Graph(id="scatter_comparison", config=DOWNLOAD_CONFIG),
                            ]
                        )
                    ],
                    width={"size": 9},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H4(id="title_triangular_heatmap_comparison"),
                                dcc.Graph(id="triangular_heatmap_comparison", config=DOWNLOAD_CONFIG),
                            ]
                        )
                    ],
                    width={"size": 9, "offset": 3},
                ),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Loading(
                            [
                                html.H4(id="title_difference_heatmap_comparison"),
                                dcc.Graph(id="difference_heatmap_comparison", config=DOWNLOAD_CONFIG),
                            ]
                        )
                    ],
                    width={"size": 9, "offset": 3},
                ),
            ]
        ),
    ],
    fluid=True,
)
