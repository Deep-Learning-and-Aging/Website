from plotly.figure_factory import create_dendrogram
from dash_website.pages.utils.heatmap import create_heatmap


def create_dendrogram_heatmap(correlations, sample_sizes):
    """
    correlations : DataFrame
        2d dataframe, with ones on the diagonal.
    samples_sizes : DataFrame
    """
    fig = create_dendrogram(correlations, orientation="bottom", distfun=lambda df: 1 - correlations)
    for scatter in fig["data"]:
        scatter["yaxis"] = "y2"

    order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))
    labels = correlations.columns[order_dendrogram]

    fig.update_layout(xaxis={"ticktext": labels, "mirror": False})
    fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})

    heat_correlations = correlations.loc[labels, labels].values
    heat_sample_sizes = sample_sizes.loc[labels, labels].values

    heatmap = create_heatmap(heat_correlations, heat_sample_sizes, labels, labels)
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