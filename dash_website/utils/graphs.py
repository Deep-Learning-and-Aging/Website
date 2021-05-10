import numpy as np
import plotly.graph_objs as go
from plotly.figure_factory import create_dendrogram

from dash_website.utils import BLUE_WHITE_RED


def heatmap_by_clustering(table_correlations, hovertemplate, customdata):
    fig = create_dendrogram(table_correlations.replace(np.nan, 0), orientation="bottom", distfun=lambda df: 1 - df)
    for scatter in fig["data"]:
        scatter["yaxis"] = "y2"

    order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))
    labels = table_correlations.columns[order_dendrogram]

    fig.update_layout(xaxis={"ticktext": labels, "mirror": False})
    fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})

    heat_correlations = table_correlations.loc[labels, labels].values
    if customdata is not None:
        heat_customdata = customdata.loc[labels, labels].values
    else:
        heat_customdata = None

    heatmap = go.Heatmap(
        x=fig["layout"]["xaxis"]["tickvals"],
        y=fig["layout"]["xaxis"]["tickvals"],
        z=heat_correlations,
        colorscale=BLUE_WHITE_RED,
        customdata=heat_customdata,
        hovertemplate=hovertemplate,
        zmin=-1,
        zmax=1,
    )

    fig.update_layout(
        yaxis={
            "domain": [0, 0.85],
            "mirror": False,
            "showgrid": False,
            "zeroline": False,
            "ticktext": labels,
            "tickvals": fig["layout"]["xaxis"]["tickvals"],
            "showticklabels": True,
            "ticks": "outside",
        }
    )

    fig.add_trace(heatmap)

    fig["layout"]["width"] = 1100
    fig["layout"]["height"] = 1100

    return fig


def heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata):
    heatmap = go.Heatmap(
        x=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
        y=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
        z=sorted_table_correlations,
        colorscale=BLUE_WHITE_RED,
        customdata=sorted_customdata,
        hovertemplate=hovertemplate,
        zmin=-1,
        zmax=1,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.columns.values],
        },
        yaxis={
            "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[0] + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.index.values],
        },
    )

    return fig


def add_custom_legend_axis(fig, sorted_table_correlations):
    dimensions = (
        sorted_table_correlations.index.to_frame()[["dimension_1", "subdimension_1"]]
        .reset_index(drop=True)
        .rename(columns={"dimension_1": "dimension", "subdimension_1": "subdimension"})
    )
    dimensions["position"] = fig["layout"]["xaxis"]["tickvals"]
    dimensions.set_index(["dimension", "subdimension"], inplace=True)

    lines = []
    annotations = []

    for dimension in dimensions.index.get_level_values("dimension").drop_duplicates():
        dimension_inner_margin = -30
        dimension_outer_margin = -60

        min_position = dimensions.loc[dimension].min()
        max_position = dimensions.loc[dimension].max()

        for first_axis, second_axis in [("x", "y"), ("y", "x")]:
            if first_axis == "x":
                textangle = 90
            else:  # first_axis == "y"
                textangle = 0

            line, annotation = add_line_and_annotation(
                dimension,
                first_axis,
                second_axis,
                min_position,
                max_position,
                dimension_inner_margin,
                dimension_outer_margin,
                textangle,
                10,
            )

            lines.append(line)
            annotations.append(annotation)

            for subdimension in dimensions.loc[dimension].index.get_level_values("subdimension").drop_duplicates():
                subdimension_margin = 0

                submin_position = dimensions.loc[(dimension, subdimension)].min()
                submax_position = dimensions.loc[(dimension, subdimension)].max()

                for first_axis, second_axis in [("x", "y"), ("y", "x")]:
                    if first_axis == "x":
                        textangle = 90
                    else:  # first_axis == "y"
                        textangle = 0

                    line, annotation = add_line_and_annotation(
                        subdimension,
                        first_axis,
                        second_axis,
                        submin_position,
                        submax_position,
                        subdimension_margin,
                        dimension_inner_margin,
                        textangle,
                        8,
                    )

                    lines.append(line)
                    annotations.append(annotation)

    # The final top/right line
    for first_axis, second_axis in [("x", "y"), ("y", "x")]:
        line, _ = add_line_and_annotation(
            dimension,
            first_axis,
            second_axis,
            min_position,
            max_position,
            0,
            dimension_outer_margin,
            0,
            10,
            final=True,
        )

        lines.append(line)

    fig["layout"]["shapes"] = lines
    fig["layout"]["annotations"] = annotations
    fig.update_layout(yaxis={"showticklabels": False}, xaxis={"showticklabels": False})

    return fig


def add_line_and_annotation(
    text, first_axis, second_axis, min_position, max_position, inner_margin, outer_margin, textangle, size, final=False
):
    if not final:
        to_match_heatmap = -10 / 2
        position = min_position
    else:
        to_match_heatmap = +10 / 2
        position = max_position
    return (
        {
            "type": "line",
            "xref": "x",
            "yref": "y",
            f"{first_axis}0": float(position + to_match_heatmap),
            f"{second_axis}0": inner_margin,
            f"{first_axis}1": float(position + to_match_heatmap),
            f"{second_axis}1": outer_margin,
            "line": {"color": "Black", "width": 0.5},
        },
        {
            "text": text,
            "xref": "x",
            "yref": "y",
            first_axis: float((min_position + max_position) / 2),
            second_axis: (inner_margin + outer_margin) / 2,
            "showarrow": False,
            "textangle": textangle,
            "font": {"size": size},
        },
    )


def histogram_correlation(table_correlations):
    correlations = table_correlations.values[np.triu_indices(table_correlations.shape[0])]
    histogram = go.Histogram(
        x=correlations,
        histnorm="percent",
    )

    fig = go.Figure(histogram)

    fig.update_layout(xaxis_title_text="Correlation", yaxis_title_text="Count (in %)", bargap=0.2, bargroupgap=0.1)
    return fig
