from plotly.graph_objs import Bar

from dash_website.pages.utils import EMPTY_GRAPH


def create_bar(correlations_mean, correlations_std):
    correlations_mean.sort_values(ascending=False, inplace=True)
    if correlations_mean.notna().sum() > 0:
        if correlations_std.notna().sum() == 0:
            return Bar(
                x=correlations_mean.index,
                y=correlations_mean,
                name="Average correlations",
                marker_color="indianred",
            )
        else:
            return Bar(
                x=correlations_mean.index,
                y=correlations_mean,
                error_y={"array": correlations_std[correlations_mean.index], "type": "data"},
                name="Average correlations",
                marker_color="indianred",
            )
    else:
        return EMPTY_GRAPH