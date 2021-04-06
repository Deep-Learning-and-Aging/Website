import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dash_website.app import APP
from dash_website.pages import (
    menu,
    page1,
    page2,
    page3,
    page4,
    page7,
    page8,
    page9,
    page10,
    page11,
    page12,
    page13,
    page14,
    page15,
    page16,
    page17,
    page18,
)

num_pages = 18


def get_server():
    add_layout(APP)
    return APP.server


def launch_local_website():
    add_layout(APP)
    APP.run_server(debug=True)


def add_layout(app):
    app.layout = html.Div(
        [
            dcc.Location(id="url", refresh=False),
            get_top_bar(),
            html.Hr(),
            html.Div(id="page_content"),
        ],
        style={"height": "100vh", "fontSize": 10},
    )


def get_top_bar():
    return html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Menu", href="/", active=True, id="menu-link")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Scalars", href="/pages/page1", id="page1-link"),
                            dbc.DropdownMenuItem("Time Series", href="/pages/page15", id="page15-link"),
                            dbc.DropdownMenuItem("Images", href="/pages/page14", id="page14-link"),
                            dbc.DropdownMenuItem("Videos", href="/pages/page16", id="page16-link"),
                        ],
                        label="Datasets",
                        nav=True,
                    ),
                    dbc.NavItem(dbc.NavLink("Age prediction performances", href="/pages/page2", id="page2-link")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Scalars", href="/pages/page3", id="page3-link"),
                            dbc.DropdownMenuItem("Time Series", href="/pages/page13", id="page13-link"),
                            dbc.DropdownMenuItem("Images", href="/pages/page9", id="page9-link"),
                            dbc.DropdownMenuItem("Videos", href="/pages/page12", id="page12-link"),
                        ],
                        label="Features importances",
                        nav=True,
                    ),
                    dbc.NavItem(
                        dbc.NavLink(
                            "Correlation between accelerated aging dimensions", href="/pages/page4", id="page4-link"
                        )
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Genetics - GWAS", href="/pages/page10", id="page10-link"),
                            dbc.DropdownMenuItem("Genetics - Heritability", href="/pages/page11", id="page11-link"),
                            dbc.DropdownMenuItem("Genetics - Correlation", href="/pages/page17", id="page17-link"),
                        ],
                        label="Genetics",
                        nav=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Univariate XWAS - Results",
                                href="/xwas/univariate_results",
                                id="xwas_univariate_results",
                            ),
                            dbc.DropdownMenuItem(
                                "Univariate XWAS - Correlations",
                                href="/xwas/univariate_correlations",
                                id="xwas_univariate_correlations",
                            ),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("Multivariate XWAS - Results", href="/pages/page7", id="page7-link"),
                            dbc.DropdownMenuItem(
                                "Multivariate XWAS - Correlations", href="/pages/page8", id="page8-link"
                            ),
                            dbc.DropdownMenuItem(
                                "Multivariate XWAS - Features importances", href="/pages/page18", id="page18-link"
                            ),
                        ],
                        label="XWAS",
                        nav=True,
                    ),
                ],
                fill=True,
                pills=True,
            ),
        ],
        style={
            "top": 0,
            "left": 50,
            "bottom": 0,
            "right": 50,
            "padding": "1rem 1rem",
        },
    )


@APP.callback(Output("page_content", "children"), Input("url", "pathname"))
def display_page(pathname):
    print(pathname)
    if "xwas" in pathname:
        if "univariate_results" in pathname:
            from dash_website.xwas.univariate_results import get_layout

            return get_layout()
        elif "univariate_correlations" in pathname:
            from dash_website.xwas.univariate_correlations import get_layout

            return get_layout()
    elif "page" in pathname:
        num_page = int(pathname.split("/")[-1][4:])
        return getattr(globals()["page%s" % num_page], "layout")
    elif pathname == "/":
        return menu.layout
    else:
        return "404"
