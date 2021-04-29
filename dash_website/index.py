from os import path
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dash_website.app import APP
from dash_website.pages import (
    page2,
    page4,
    page10,
    page11,
    page17,
)


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
                    dbc.NavItem(dbc.NavLink("Introduction", href="/", active=True, id="introduction")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Scalars", href="/datasets/scalars", id="datasets_scalars"),
                            dbc.DropdownMenuItem(
                                "Time Series", href="/datasets/time_series", id="datasets_time_series"
                            ),
                            dbc.DropdownMenuItem("Images", href="/datasets/images", id="datasets_images"),
                            dbc.DropdownMenuItem("Videos", href="/datasets/videos", id="datasets_videos"),
                        ],
                        label="Datasets",
                        nav=True,
                    ),
                    dbc.NavItem(dbc.NavLink("Age prediction performances", href="/pages/page2", id="page2-link")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Scalars", href="/feature_importances/scalars", id="feature_importances_scalars"
                            ),
                            dbc.DropdownMenuItem(
                                "Time Series",
                                href="/feature_importances/time_series",
                                id="feature_importances_time_series",
                            ),
                            dbc.DropdownMenuItem(
                                "Images", href="/feature_importances/images", id="feature_importances_images"
                            ),
                            dbc.DropdownMenuItem(
                                "Videos", href="/feature_importances/videos", id="feature_importances_videos"
                            ),
                        ],
                        label="Feature importances",
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
                            dbc.DropdownMenuItem(
                                "Multivariate XWAS - Results",
                                href="/xwas/multivariate_results",
                                id="xwas_multivariate_results",
                            ),
                            dbc.DropdownMenuItem(
                                "Multivariate XWAS - Correlations",
                                href="/xwas/multivariate_correlations",
                                id="xwas_multivariate_correlations",
                            ),
                            dbc.DropdownMenuItem(
                                "Multivariate XWAS - Feature importances",
                                href="/xwas/multivariate_feature_importances",
                                id="xwas_multivariate_feature_importances",
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
    if "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            from dash_website.datasets.scalars import get_layout
        elif "time_series" == pathname.split("/")[2]:
            from dash_website.datasets.time_series import get_layout
        elif "images" == pathname.split("/")[2]:
            from dash_website.datasets.images import get_layout
        elif "videos" == pathname.split("/")[2]:
            from dash_website.datasets.videos import get_layout

        return get_layout()
    elif "feature_importances" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            from dash_website.feature_importances.scalars import get_layout
        elif "time_series" == pathname.split("/")[2]:
            from dash_website.feature_importances.time_series import get_layout
        elif "images" == pathname.split("/")[2]:
            from dash_website.feature_importances.images import get_layout
        elif "videos" == pathname.split("/")[2]:
            from dash_website.feature_importances.videos import get_layout

        return get_layout()
    elif "xwas" == pathname.split("/")[1]:
        if "univariate_results" == pathname.split("/")[2]:
            from dash_website.xwas.univariate_results import get_layout
        elif "univariate_correlations" == pathname.split("/")[2]:
            from dash_website.xwas.univariate_correlations import get_layout
        elif "multivariate_results" == pathname.split("/")[2]:
            from dash_website.xwas.multivariate_results import get_layout
        elif "multivariate_correlations" == pathname.split("/")[2]:
            from dash_website.xwas.multivariate_correlations import get_layout
        elif "multivariate_feature_importances" == pathname.split("/")[2]:
            from dash_website.xwas.multivariate_feature_importances import get_layout

        return get_layout()

    elif "page" in pathname:
        num_page = int(pathname.split("/")[-1][4:])
        return getattr(globals()["page%s" % num_page], "layout")
    elif "/" == pathname:
        from dash_website.introduction.introduction import get_layout

        return get_layout()
    else:
        return "404"
