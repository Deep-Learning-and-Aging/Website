from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output

from dash_website.genetics.gwas_tabs.manhattan_qq import get_manhattan_qq
from dash_website.genetics.gwas_tabs.volcano import get_volcano


def get_layout():
    return html.Div(
        [
            dbc.Tabs(
                [
                    dbc.Tab(label="Select Manhattan & QQ plots", tab_id="tab_manhatton_qq_gwas"),
                    dbc.Tab(label="Select Volcano plot", tab_id="tab_volcano_gwas"),
                ],
                id="tab_manager_gwas",
                active_tab="tab_manhatton_qq_gwas",
            ),
            html.Div(id="tab_content_gwas"),
        ]
    )


@APP.callback(Output("tab_content_gwas", "children"), Input("tab_manager_gwas", "active_tab"))
def _fill_tab(
    active_tab,
):
    if active_tab == "tab_manhatton_qq_gwas":
        return get_manhattan_qq()
    else:  # active_tab == "tab_volcano_gwas":
        return get_volcano()
