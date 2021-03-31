import numpy as np


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