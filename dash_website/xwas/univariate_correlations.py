from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.utils.aws_loader import load_feather
from dash_website.xwas.univariate_correlations_tabs.category_heatmap import get_category_heatmap
from dash_website.xwas.univariate_correlations_tabs.dimension_heatmap import get_dimension_heatmap
from dash_website.xwas.univariate_correlations_tabs.average_bars import get_average_bars
from dash_website.utils.controls import get_subset_method_radio_items, get_correlation_type_radio_items


def get_layout():
    return html.Div(
        [
            dcc.Store(
                id="store_subset_method_correlation_type",
                data=[
                    get_subset_method_radio_items("subset_method_correlations"),
                    get_correlation_type_radio_items("correlation_type_correlations"),
                ],
            ),
            dcc.Loading(
                [
                    dcc.Store(id="memory_correlations"),
                    dcc.Store(id="memory_number_variables"),
                ]
            ),
            dbc.Tabs(
                [
                    dbc.Tab(label="Select Category", tab_id="tab_category"),
                    dbc.Tab(label="Select Dimension", tab_id="tab_dimension"),
                    dbc.Tab(label="Select Average", tab_id="tab_average"),
                ],
                id="tab_manager_correlations",
                active_tab="tab_category",
            ),
            html.Div(id="tab_content_correlations"),
        ]
    )


@APP.callback(
    Output("store_subset_method_correlation_type", "data"),
    [Input("subset_method_correlations", "value"), Input("correlation_type_correlations", "value")],
)
def update_commun_subset_method_correlation_type(subset_method, correlation_type):
    return [
        get_subset_method_radio_items("subset_method_correlations", subset_method),
        get_correlation_type_radio_items("correlation_type_correlations", correlation_type),
    ]


@APP.callback(
    Output("memory_correlations", "data"),
    [Input("subset_method_correlations", "value"), Input("correlation_type_correlations", "value")],
)
def _modify_store_correlations(subset_method, correlation_type):
    return load_feather(
        f"xwas/univariate_correlations/correlations/correlations_{subset_method}_{correlation_type}.feather"
    ).to_dict()


@APP.callback(Output("memory_number_variables", "data"), Input("subset_method_correlations", "value"))
def _modify_store_number_variables(subset_method):
    return load_feather(f"xwas/univariate_correlations/correlations/number_variables_{subset_method}.feather").to_dict()


@APP.callback(
    Output("tab_content_correlations", "children"),
    [Input("tab_manager_correlations", "active_tab"), Input("store_subset_method_correlation_type", "data")],
)
def _fill_tab(active_tab, subset_method_correlation_type):
    subset_method_radio_items, correlation_type_radio_items = subset_method_correlation_type
    if active_tab == "tab_category":
        return get_category_heatmap(subset_method_radio_items, correlation_type_radio_items)
    elif active_tab == "tab_dimension":
        return get_dimension_heatmap(subset_method_radio_items, correlation_type_radio_items)
    else:  # active_tab == "tab_average"
        return get_average_bars(subset_method_radio_items, correlation_type_radio_items)
