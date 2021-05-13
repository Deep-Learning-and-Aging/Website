from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.xwas.multivariate_correlations_tabs.category_heatmap_multi import get_category_heatmap
from dash_website.xwas.multivariate_correlations_tabs.dimension_heatmap_multi import get_dimension_heatmap
from dash_website.xwas.multivariate_correlations_tabs.average_bars_multi import get_average_bars


@APP.callback(
    Output("tab_content_correlations_multi", "children"), Input("tab_manager_correlations_multi", "active_tab")
)
def _fill_tab(
    active_tab,
):
    if active_tab == "tab_category_multi":
        return get_category_heatmap()
    elif active_tab == "tab_dimension_multi":
        return get_dimension_heatmap()
    else:  # active_tab == "tab_average_multi"
        return get_average_bars()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Select Category", tab_id="tab_category_multi"),
                dbc.Tab(label="Select Dimension", tab_id="tab_dimension_multi"),
                dbc.Tab(label="Select Average", tab_id="tab_average_multi"),
            ],
            id="tab_manager_correlations_multi",
            active_tab="tab_category_multi",
        ),
        html.Div(id="tab_content_correlations_multi"),
    ]
)
