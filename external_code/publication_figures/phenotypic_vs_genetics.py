import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.graphs import heatmap_by_sorted_dimensions
from dash_website import DOWNLOAD_CONFIG, GRAPH_SIZE


def get_data_upper_comparison(uni_or_multi, category):
    return load_feather(
        f"xwas/{uni_or_multi}_correlations/correlations/categories/correlations_{category}.feather"
    ).to_dict()


def get_graph_comparison(data_comparison_upper, data_comparison_lower):
    table_correlations_upper, customdata_upper, _ = get_table_and_customdata(data_comparison_upper)
    np.fill_diagonal(table_correlations_upper.values, np.nan)

    table_correlations_lower, customdata_lower, _ = get_table_and_customdata(data_comparison_lower)
    np.fill_diagonal(table_correlations_lower.values, np.nan)

    subdimension_order = ["*", "FullBody", "Spine", "Hips", "Knees", "Scalars"]
    sorted_dimensions = table_correlations_lower.sort_index(
        axis=0,
        level=1,
        key=lambda subdimensions: list(map(lambda subdimension: subdimension_order.index(subdimension), subdimensions)),
    ).index

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

    fig_triangular.update_layout(
        yaxis={
            "title": "Phenotypic correlation",
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 25},
            "ticktext": [elem[1] for elem in triangular_heatmap.columns.values],
        },
        xaxis={
            "title": "Genetics correlation",
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 25},
            "ticktext": [elem[1] for elem in triangular_heatmap.index.values],
            "tickangle": 90,
        },
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return fig_triangular


def get_table_and_customdata(data_comparison):
    correlations_raw = pd.DataFrame(data_comparison).set_index(
        ["dimension_1", "subdimension_1", "r2_1", "r2_std_1", "dimension_2", "subdimension_2", "r2_2", "r2_std_2"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["method", "correlation_type"]
    )
    correlations = correlations_raw[[("union", "pearson"), ("union", "number_variables")]]
    correlations.columns = ["correlation", "number_variables"]
    correlations.reset_index(inplace=True)

    correlations = correlations[
        (correlations["dimension_1"] == "Musculoskeletal") & (correlations["dimension_2"] == "Musculoskeletal")
    ]

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1"],
        columns=["dimension_2", "subdimension_2"],
        values="correlation",
    ).loc[ORDER_DIMENSIONS, ORDER_DIMENSIONS]

    customdata_list = []
    for customdata_item in ["r2_1", "r2_std_1", "r2_2", "r2_std_2", "number_variables"]:
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


if __name__ == "__main__":
    ORDER_DIMENSIONS = pd.MultiIndex.from_tuples(
        [
            ("Musculoskeletal", "*"),
            ("Musculoskeletal", "FullBody"),
            ("Musculoskeletal", "Hips"),
            ("Musculoskeletal", "Knees"),
            ("Musculoskeletal", "Scalars"),
            ("Musculoskeletal", "Spine"),
        ]
    )
    upper_comparison = get_data_upper_comparison(uni_or_multi="univariate", category="Genetics")
    lower_comparison = get_data_upper_comparison(uni_or_multi="univariate", category="Phenotypic")

    fig_triangular = get_graph_comparison(upper_comparison, lower_comparison)

    fig_triangular.show(config=DOWNLOAD_CONFIG)
