from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.xwas.multivariate_correlations_tabs.category_heatmap_multi import get_heatmap_multivariate_category
from dash_website.xwas.multivariate_correlations_tabs.dimension_heatmap_multi import get_dimension_heatmap
from dash_website.xwas.multivariate_correlations_tabs.average_bars_multi import get_average_bars_multivariate


@APP.callback(
    Output("tab_content_multivariate", "children"),
    Input("tab_manager_multivariate", "active_tab"),
)
def _fill_tab(
    active_tab,
):
    if active_tab == "tab_category_multivariate":
        return get_heatmap_multivariate_category()
    elif active_tab == "tab_dimension_multivariate":
        return get_dimension_heatmap()
    else:  # active_tab == "tab_average_multi"
        return get_average_bars_multivariate()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="By category", tab_id="tab_category_multivariate"),
                dbc.Tab(label="By aging dimension", tab_id="tab_dimension_multivariate"),
                dbc.Tab(label="Summary", tab_id="tab_average_multivariate"),
            ],
            id="tab_manager_multivariate",
            active_tab="tab_category_multivariate",
        ),
        html.Div(id="tab_content_multivariate"),
    ]
)
