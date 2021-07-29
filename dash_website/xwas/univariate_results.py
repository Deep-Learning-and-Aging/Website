import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.app import APP
from dash_website.xwas.univariate_results_tabs.volcano import get_univariate_volcano
from dash_website.xwas.univariate_results_tabs.summary import get_univariate_summary


@APP.callback(
    Output("tab_content_univariate_results", "children"), Input("tab_manager_univariate_results", "active_tab")
)
def _get_tab_univariate_results(active_tab):
    if active_tab == "tab_univariate_volcano":
        return get_univariate_volcano()
    else:  # active_tab == "tab_summary"
        return get_univariate_summary()


LAYOUT = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(label="Volcano", tab_id="tab_univariate_volcano"),
                dbc.Tab(label="Summary", tab_id="tab_univariate_summary"),
            ],
            id="tab_manager_univariate_results",
            active_tab="tab_univariate_volcano",
        ),
        html.Div(id="tab_content_univariate_results"),
    ]
)
