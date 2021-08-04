from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.utils.aws_loader import load_feather
from dash_website.xwas.multivariate_results_tabs.heatmap import get_heatmap_multivariate_results
from dash_website.xwas.multivariate_results_tabs.bar_plot import get_bar_plot_multivariate_results


@APP.callback(
    Output("tab_content_multivariate_results", "children"), Input("tab_manager_multivariate_results", "active_tab")
)
def _fill_tab_multivariate_results(
    active_tab,
):
    if active_tab == "tab_heatmap_multivariate_results":
        return get_heatmap_multivariate_results()
    else:  # active_tab == "tab_bar_plot"
        return get_bar_plot_multivariate_results()


LAYOUT = html.Div(
    [
        dcc.Loading(
            dcc.Store(
                id="memory_scores_multivariate_results",
                data=load_feather("xwas/multivariate_results/scores.feather").to_dict(),
            )
        ),
        dbc.Tabs(
            [
                dbc.Tab(label="View heatmap", tab_id="tab_heatmap_multivariate_results"),
                dbc.Tab(label="View bar plot", tab_id="tab_bar_plot_multivariate_results"),
            ],
            id="tab_manager_multivariate_results",
            active_tab="tab_heatmap_multivariate_results",
        ),
        html.Div(id="tab_content_multivariate_results"),
    ]
)
