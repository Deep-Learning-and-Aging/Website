from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.correlation_between.correlation_between_tabs.all_dimensions import get_all_dimensions
from dash_website.correlation_between.correlation_between_tabs.custom_dimensions import get_custom_dimensions


@APP.callback(
    Output("tab_content_correlation_between", "children"), Input("tab_manager_correlation_between", "active_tab")
)
def _fill_tab(
    active_tab,
):
    if active_tab == "tab_custom_dimensions_correlation_between":
        return get_custom_dimensions()
    else:  # active_tab == "tab_all_dimensions_correlation_between":
        return get_all_dimensions()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="33 principal aging dimensions", tab_id="tab_custom_dimensions_correlation_between"),
                dbc.Tab(label="All 331 aging dimensions", tab_id="tab_all_dimensions_correlation_between"),
            ],
            id="tab_manager_correlation_between",
            active_tab="tab_custom_dimensions_correlation_between",
        ),
        html.Div(id="tab_content_correlation_between"),
    ]
)
