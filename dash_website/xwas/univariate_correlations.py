from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.xwas.univariate_correlations_tabs.category_heatmap import get_heatmap_univariate_category
from dash_website.xwas.univariate_correlations_tabs.dimension_heatmap import get_heatmap_univariate_dimension
from dash_website.xwas.univariate_correlations_tabs.average_bars import get_univariate_average_bars


@APP.callback(
    Output("tab_content_univariate_correlations", "children"),
    Input("tab_manager_univariate_correlations", "active_tab"),
)
def _get_tab_univariate_correlations(
    active_tab,
):
    if active_tab == "tab_univariate_category":
        return get_heatmap_univariate_category()
    elif active_tab == "tab_univariate_dimension":
        return get_heatmap_univariate_dimension()
    else:  # active_tab == "tab_average"
        return get_univariate_average_bars()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="By category", tab_id="tab_univariate_category"),
                dbc.Tab(label="By aging dimension", tab_id="tab_univariate_dimension"),
                dbc.Tab(label="Summary", tab_id="tab_univariate_average"),
            ],
            id="tab_manager_univariate_correlations",
            active_tab="tab_univariate_category",
        ),
        html.Div(id="tab_content_univariate_correlations"),
    ]
)
