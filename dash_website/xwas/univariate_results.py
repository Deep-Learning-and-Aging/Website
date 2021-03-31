import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.app import APP
from dash_website.xwas.univariate_results_tabs.volcano import get_volcano
from dash_website.xwas.univariate_results_tabs.summary import get_summary


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Volcano", tab_id="tab_volcano"),
                    dbc.Tab(label="Summary", tab_id="tab_summary"),
                ],
                id="tab_manager_results",
                active_tab="tab_summary",
            ),
            html.Div(id="tab_content_results"),
        ]
    )


@APP.callback(Output("tab_content_results", "children"), Input("tab_manager_results", "active_tab"))
def _get_tab(active_tab):
    if active_tab == "tab_volcano":
        return get_volcano()
    else:  # active_tab == "tab_summary"
        return get_summary()