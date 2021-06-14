import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.graphs import heatmap_by_sorted_dimensions, add_line_and_annotation
from dash_website import DOWNLOAD_CONFIG, GRAPH_SIZE
from dash_website.correlation_between import SAMPLE_DEFINITION


def get_data_all_dimensions(sample_definition):
    return load_feather(
        f"correlation_between_accelerated_aging_dimensions/all_dimensions_{sample_definition}.feather"
    ).to_dict()


def get_graph_all_dimensions(selected_dimension, data_all_dimensions):
    correlations = pd.DataFrame(data_all_dimensions)
    correlations = correlations[
        (correlations["dimension_1"] == selected_dimension) & (correlations["dimension_2"] == selected_dimension)
    ]

    table_correlations = correlations.pivot(
        index=["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"],
        columns=["dimension_2", "subdimension_2", "sub_subdimension_2", "algorithm_2"],
        values="correlation",
    )
    order_dimensions = table_correlations.index
    table_correlations = table_correlations.loc[order_dimensions, order_dimensions]
    np.fill_diagonal(table_correlations.values, np.nan)

    customdata_list = []
    for customdata_item in ["correlation_std", "r2_1", "r2_std_1", "r2_2", "r2_std_2"]:
        customdata_list.append(
            correlations.pivot(
                index=["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"],
                columns=["dimension_2", "subdimension_2", "sub_subdimension_2", "algorithm_2"],
                values=customdata_item,
            )
            .loc[order_dimensions, order_dimensions]
            .values
        )
    stacked_customdata = list(map(list, np.dstack(customdata_list)))

    customdata = pd.DataFrame(None, index=order_dimensions, columns=order_dimensions)
    customdata[customdata.columns] = stacked_customdata

    hovertemplate = "Correlation: %{z:.3f} +- %{customdata[0]:.3f} <br><br>Dimensions 1: %{x} <br>R²: %{customdata[1]:.3f} +- %{customdata[2]:.3f} <br>Dimensions 2: %{y} <br>R²: %{customdata[3]:.3f} +- %{customdata[4]:.3f}<br><extra></extra>"

    subdimension_order = ["*", "FullBody", "Spine", "Hips", "Knees", "Scalars"]
    sorted_dimensions = table_correlations.sort_index(
        axis=0,
        level=1,
        key=lambda subdimensions: list(map(lambda subdimension: subdimension_order.index(subdimension), subdimensions)),
    ).index

    sorted_table_correlations = table_correlations.loc[sorted_dimensions, sorted_dimensions]
    sorted_customdata = customdata.loc[sorted_dimensions, sorted_dimensions]

    fig = heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata)

    fig.update_layout(
        xaxis={"tickvals": np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10)},
        yaxis={"tickvals": np.arange(5, 10 * sorted_table_correlations.shape[0] + 5, 10)},
    )

    dimensions = (
        sorted_table_correlations.index.to_frame()[["dimension_1", "subdimension_1", "sub_subdimension_1"]]
        .reset_index(drop=True)
        .rename(
            columns={
                "dimension_1": "dimension",
                "subdimension_1": "subdimension",
                "sub_subdimension_1": "sub_subdimension",
            }
        )
    )
    dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
    dimensions.set_index(["dimension", "subdimension", "sub_subdimension"], inplace=True)

    lines = []
    annotations = []

    dimension_inner_margin = -150
    subdimension_margin = -100
    sub_subdimension_margin = 0

    textangles = {"x": 90, "y": 0}

    min_position = dimensions.loc[selected_dimension].min()
    max_position = dimensions.loc[selected_dimension].max()

    for subdimension in dimensions.loc[selected_dimension].index.get_level_values("subdimension").drop_duplicates():
        submin_position = dimensions.loc[(selected_dimension, subdimension)].min()
        submax_position = dimensions.loc[(selected_dimension, subdimension)].max()

        for first_axis, second_axis in [("x", "y"), ("y", "x")]:
            line, annotation = add_line_and_annotation(
                subdimension,
                first_axis,
                second_axis,
                submin_position,
                submax_position,
                subdimension_margin,
                dimension_inner_margin,
                textangles[first_axis],
                18,
            )

            lines.append(line)
            annotations.append(annotation)

            if selected_dimension == "all":
                continue

            for sub_subdimension in (
                dimensions.loc[(selected_dimension, subdimension)]
                .index.get_level_values("sub_subdimension")
                .drop_duplicates()
            ):
                sub_submin_position = dimensions.loc[(selected_dimension, subdimension, sub_subdimension)].min()
                sub_submax_position = dimensions.loc[(selected_dimension, subdimension, sub_subdimension)].max()

                for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                    line, annotation = add_line_and_annotation(
                        sub_subdimension,
                        first_axis,
                        second_axis,
                        sub_submin_position,
                        sub_submax_position,
                        sub_subdimension_margin,
                        subdimension_margin,
                        textangles[first_axis],
                        16,
                    )

                    lines.append(line)
                    annotations.append(annotation)

    # The final top/right line
    for first_axis, second_axis in [("x", "y"), ("y", "x")]:
        line, _ = add_line_and_annotation(
            selected_dimension,
            first_axis,
            second_axis,
            min_position,
            max_position,
            0,
            dimension_inner_margin,
            0,
            10,
            final=True,
        )

        lines.append(line)

    fig["layout"]["shapes"] = lines
    fig["layout"]["annotations"] = annotations

    fig.update_layout(yaxis={"showticklabels": False}, xaxis={"showticklabels": False})
    fig.update_layout(
        yaxis={"showgrid": False, "zeroline": False, "title_font": {"size": 25}},
        xaxis={"showgrid": False, "zeroline": False, "title_font": {"size": 25}},
        width=GRAPH_SIZE,
        height=GRAPH_SIZE,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return fig


if __name__ == "__main__":
    sample_definiion = list(SAMPLE_DEFINITION.keys())[2]
    print("Sample definition: ", sample_definiion)
    data_all_dimensions = get_data_all_dimensions(sample_definiion)

    fig_musculoskeletal = get_graph_all_dimensions("Musculoskeletal", data_all_dimensions)

    fig_musculoskeletal.show(config=DOWNLOAD_CONFIG)
