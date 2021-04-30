from plotly.graph_objs import Heatmap
from plotly.figure_factory import create_dendrogram
from dash_website.utils.graphs.colorscale import get_colorscale


def create_dendrogram_heatmap(correlations, sample_sizes, size_label_is_variable=True):
    """
    correlations : DataFrame
        2d dataframe.
    samples_sizes : DataFrame
        2d dataframe.
    """
    fig = create_dendrogram(correlations, orientation="bottom", distfun=lambda df: 1 - df)
    for scatter in fig["data"]:
        scatter["yaxis"] = "y2"

    order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))
    labels = correlations.columns[order_dendrogram]

    fig.update_layout(xaxis={"ticktext": labels, "mirror": False})
    fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})

    heat_correlations = correlations.loc[labels, labels].values
    heat_sample_sizes = sample_sizes.loc[labels, labels].values

    if size_label_is_variable:
        hovertemplate = "Correlation: %{z:.3f} <br>Dimension 1: %{x} <br>Dimension 2: %{y} <br>Number variables: %{customdata} <br><extra></extra>"
    else:
        hovertemplate = "Correlation: %{z:.3f} <br>Dimension 1: %{x} <br>Dimension 2: %{y} <br>Number features: %{customdata} <br><extra></extra>"

    heatmap = Heatmap(
        x=labels,
        y=labels,
        z=heat_correlations,
        colorscale=get_colorscale(heat_correlations),
        customdata=heat_sample_sizes,
        hovertemplate=hovertemplate,
        zmin=-1,
        zmax=1,
    )
    heatmap["x"] = fig["layout"]["xaxis"]["tickvals"]
    heatmap["y"] = fig["layout"]["xaxis"]["tickvals"]

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