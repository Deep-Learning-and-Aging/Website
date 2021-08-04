import numpy as np
import plotly.graph_objs as go
from plotly.figure_factory import create_dendrogram

from dash_website import GRAPH_SIZE
from dash_website.utils import BLUE_WHITE_RED, MAX_LENGTH_CATEGORY


def heatmap_by_clustering(table_correlations, hovertemplate, customdata, zmin=-1, zmax=1):
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
        zmin=zmin,
        zmax=zmax,
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
            "tickfont": {"size": 15},
        },
        xaxis={"tickfont": {"size": 15}},
    )

    fig.add_trace(heatmap)

    fig["layout"]["width"] = 1100
    fig["layout"]["height"] = 1100

    return fig


def heatmap_by_sorted_dimensions(sorted_table_correlations, hovertemplate, sorted_customdata, zmin=-1, zmax=1):
    heatmap = go.Heatmap(
        x=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
        y=np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
        z=sorted_table_correlations,
        colorscale=BLUE_WHITE_RED,
        customdata=sorted_customdata,
        hovertemplate=hovertemplate,
        zmin=zmin,
        zmax=zmax,
    )

    fig = go.Figure(heatmap)

    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[1] + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.columns.values],
            "tickfont": {"size": 15},
        },
        yaxis={
            "tickvals": np.arange(5, 10 * sorted_table_correlations.shape[0] + 5, 10),
            "ticktext": [" - ".join(elem) for elem in sorted_table_correlations.index.values],
            "tickfont": {"size": 15},
        },
    )

    return fig


def add_custom_legend_axis(
    fig,
    indexes,
    outer_margin_level_1=-60,
    inner_margin_level_1=-30,
    margin_level_2=0,
    size_level_1=11,
    size_level_2=9,
    horizontal=True,
):
    name_level_1, name_level_2 = indexes.names[:2]
    indexes_info = indexes.to_frame()[[name_level_1, name_level_2]].reset_index(drop=True)
    if horizontal:
        indexes_info["position"] = fig["layout"]["xaxis"]["tickvals"]
    else:
        indexes_info["position"] = fig["layout"]["yaxis"]["tickvals"]
    indexes_info.set_index([name_level_1, name_level_2], inplace=True)

    lines = []
    annotations = []

    for level_1 in indexes_info.index.get_level_values(name_level_1).drop_duplicates():
        min_position = indexes_info.loc[level_1].min()
        max_position = indexes_info.loc[level_1].max()

        line, annotation = add_line_and_annotation(
            level_1, min_position, max_position, inner_margin_level_1, outer_margin_level_1, size_level_1, horizontal
        )

        lines.append(line)
        annotations.append(annotation)

        for level_2 in indexes_info.loc[level_1].index.get_level_values(name_level_2).drop_duplicates():
            submin_position = indexes_info.loc[(level_1, level_2)].min()
            submax_position = indexes_info.loc[(level_1, level_2)].max()

            line, annotation = add_line_and_annotation(
                level_2,
                submin_position,
                submax_position,
                margin_level_2,
                inner_margin_level_1,
                size_level_2,
                horizontal,
            )

            lines.append(line)
            annotations.append(annotation)

    # The final top/right line
    line, _ = add_line_and_annotation(
        level_1,
        min_position,
        max_position,
        margin_level_2,
        outer_margin_level_1,
        size_level_2,
        horizontal,
        final=True,
    )

    lines.append(line)

    if fig["layout"]["shapes"] == ():
        fig["layout"]["shapes"] = lines
        fig["layout"]["annotations"] = annotations
    else:
        fig["layout"]["shapes"] = list(fig["layout"]["shapes"]) + lines
        fig["layout"]["annotations"] = list(fig["layout"]["annotations"]) + annotations

    fig.update_layout(yaxis={"showticklabels": False}, xaxis={"showticklabels": False})

    return fig


def add_line_and_annotation(
    text, min_position, max_position, inner_margin, outer_margin, size, horizontal, final=False
):
    if horizontal:
        textangle = 90
        first_axis, second_axis = ["x", "y"]
    else:
        textangle = 0
        first_axis, second_axis = ["y", "x"]

    if not final:
        to_match_heatmap = -10 / 2
        position = min_position
    else:
        to_match_heatmap = +10 / 2
        position = max_position

    if len(text) > MAX_LENGTH_CATEGORY:
        text = text[:MAX_LENGTH_CATEGORY] + "..."

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
    correlations = table_correlations.values[np.triu_indices(table_correlations.shape[0], k=1)]
    histogram = go.Histogram(x=correlations, histnorm="percent", xbins={"size": 0.01})

    fig = go.Figure(histogram)

    fig.update_layout(
        height=500,
        width=GRAPH_SIZE,
        xaxis_title_text="Correlation",
        xaxis_title_font={"size": 25},
        yaxis_title_text="Count (in %)",
        yaxis_title_font={"size": 25},
        bargap=0.2,
        bargroupgap=0.1,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )
    return fig
