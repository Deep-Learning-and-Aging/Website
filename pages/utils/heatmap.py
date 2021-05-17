import numpy as np
from plotly.graph_objs import Heatmap


def f(x):
    if x <= 0:
        x1 = 255 * (x + 1)
        x1 = round(x1, 5)
        return "rgba(%s, %s, %s, 0.85)" % (255, int(x1), int(x1))
    else:
        x2 = 255 * (1 - x)
        x2 = round(x2, 5)
        return "rgba(%s, %s, %s, 0.85)" % (int(x2), int(x2), 255)


def get_colorscale(df):
    min = df.min().min()
    max = df.max().max()
    abs = np.abs(min / (min - max))
    if abs > 1:
        colorscale = [[0, f(min)], [1, f(max)]]
    else:
        colorscale = [[0, f(min)], [abs, "rgba(255, 255, 255, 0.85)"], [1, f(max)]]
    return colorscale


def create_heatmap(heat_correlations, heat_sample_sizes, labels_x, labels_y):
    colorscale = get_colorscale(heat_correlations)

    hovertemplate = "Correlation : %{z} <br>Organ x : %{x} <br>Organ y : %{y} <br>Sample Size : %{customdata}"

    return Heatmap(
        x=labels_x,
        y=labels_y,
        z=heat_correlations,
        colorscale=colorscale,
        customdata=heat_sample_sizes,
        hovertemplate=hovertemplate,
    )