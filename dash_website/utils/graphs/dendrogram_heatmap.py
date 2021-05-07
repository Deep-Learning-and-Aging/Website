import numpy as np
from plotly.graph_objs import Heatmap
from plotly.figure_factory import create_dendrogram

from dash_website.utils import BLUE_WHITE_RED


def create_dendrogram_heatmap(correlations, hovertemplate, customdata=None):
    """
    correlations : DataFrame
        2d dataframe.
    samples_sizes : DataFrame
        2d dataframe.
    """
    fig = create_dendrogram(correlations.replace(np.nan, 0), orientation="bottom", distfun=lambda df: 1 - df)
    for scatter in fig["data"]:
        scatter["yaxis"] = "y2"

    order_dendrogram = list(map(int, fig["layout"]["xaxis"]["ticktext"]))
    labels = correlations.columns[order_dendrogram]

    fig.update_layout(xaxis={"ticktext": labels, "mirror": False})
    fig.update_layout(yaxis2={"domain": [0.85, 1], "showticklabels": False, "showgrid": False, "zeroline": False})

    heat_correlations = correlations.loc[labels, labels].values
    if customdata is not None:
        heat_customdata = customdata.loc[labels, labels].values
    else:
        heat_customdata = None

    heatmap = Heatmap(
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