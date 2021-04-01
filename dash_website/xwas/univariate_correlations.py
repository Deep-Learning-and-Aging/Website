from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.utils.aws_loader import load_feather
from dash_website.xwas.univariate_correlations_tabs.category_heatmap import get_category_heatmap
from dash_website.xwas.univariate_correlations_tabs.dimension_heatmap import get_dimension_heatmap
from dash_website.xwas.univariate_correlations_tabs.average_bars import get_average_bars


def get_layout():
    return html.Div(
        [
            dcc.Store(id="memory_correlations"),
            dbc.Tabs(
                [
                    dbc.Tab(label="Select Category", tab_id="tab_category"),
                    dbc.Tab(label="Select Dimension", tab_id="tab_dimension"),
                    dbc.Tab(label="Select Average", tab_id="tab_average"),
                ],
                id="tab_manager_correlations",
                active_tab="tab_average",
            ),
            html.Div(id="tab_content_correlations"),
        ]
    )


@APP.callback(Output("tab_content_correlations", "children"), Input("tab_manager_correlations", "active_tab"))
def _fill_tab(active_tab):
    if active_tab == "tab_category":
        return get_category_heatmap()
    elif active_tab == "tab_dimension":
        return get_dimension_heatmap()
    else:  # active_tab == "tab_average"
        return get_average_bars()


@APP.callback(Output("memory_correlations", "data"), Input("subset_method_correlations", "value"))
def _modify_store_category(subset_method):
    return load_feather(f"xwas/univariate_correlations/averages_correlations_{subset_method}.feather").to_dict()
