from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.xwas.multivariate_results_tabs.heatmap import get_heatmap
from dash_website.xwas.multivariate_results_tabs.bar_plot import get_bar_plot


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="View heatmap", tab_id="tab_heatmap"),
                    dbc.Tab(label="View bar plot", tab_id="tab_bar_plot"),
                ],
                id="tab_manager_multi_results",
                active_tab="tab_heatmap",
            ),
            html.Div(id="tab_content_multi_results"),
        ]
    )


@APP.callback(Output("tab_content_multi_results", "children"), Input("tab_manager_multi_results", "active_tab"))
def _fill_tab(
    active_tab,
):
    if active_tab == "tab_heatmap":
        return get_heatmap()
    else:  # active_tab == "tab_bar_plot"
        return get_bar_plot()
