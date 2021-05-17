import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from dash_website.app import APP

import dash_website.datasets.scalars as datasets_scalars
import dash_website.datasets.time_series as datasets_time_series
import dash_website.datasets.images as datasets_images
import dash_website.datasets.videos as datasets_videos

import dash_website.age_prediction_performances.age_prediction_performances as age_prediction_performances

import dash_website.feature_importances.scalars as feature_importances_scalars
import dash_website.feature_importances.time_series as feature_importances_time_series
import dash_website.feature_importances.images as feature_importances_images
import dash_website.feature_importances.videos as feature_importances_videos

import dash_website.correlation_between.correlation_between as correlation_between

import dash_website.genetics.gwas as genetics_gwas
import dash_website.genetics.correlations as genetics_correlations
import dash_website.genetics.heritability as genetics_heritability

import dash_website.xwas.univariate_results as xwas_univariate_results
import dash_website.xwas.univariate_correlations as xwas_univariate_correlations
import dash_website.xwas.multivariate_results as xwas_multivariate_results
import dash_website.xwas.multivariate_correlations as xwas_multivariate_correlations
import dash_website.xwas.multivariate_feature_importances as xwas_multivariate_feature_importances

import dash_website.correlations_comparison.correlations_comparison as correlations_comparison

import dash_website.introduction.introduction as introduction


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
                    dbc.NavItem(
                        dbc.NavLink(
                            "Age prediction performances",
                            href="/age_prediction_performances",
                            id="age_prediction_performances",
                        )
                    ),
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
                            "Correlation between accelerated aging dimensions",
                            href="/correlation_between",
                            id="correlation_between",
                        )
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Genetics - GWAS", href="/genetics/gwas", id="genetics_gwas"),
                            dbc.DropdownMenuItem(
                                "Genetics - Heritability", href="/genetics/heritability", id="genetics_heritability"
                            ),
                            dbc.DropdownMenuItem(
                                "Genetics - Correlation", href="/genetics/correlations", id="genetics_correlations"
                            ),
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
                    dbc.NavItem(
                        dbc.NavLink(
                            "Correlations comparison",
                            href="/correlations_comparison",
                            id="correlations_comparison",
                        )
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
def _display_page(pathname):
    if "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            layout = datasets_scalars.LAYOUT

        elif "time_series" == pathname.split("/")[2]:
            layout = datasets_time_series.LAYOUT
        elif "images" == pathname.split("/")[2]:
            layout = datasets_images.LAYOUT
        elif "videos" == pathname.split("/")[2]:
            layout = datasets_videos.LAYOUT

    elif "age_prediction_performances" == pathname.split("/")[1]:
        layout = age_prediction_performances.LAYOUT

    elif "feature_importances" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            layout = feature_importances_scalars.LAYOUT
        elif "time_series" == pathname.split("/")[2]:
            layout = feature_importances_time_series.LAYOUT
        elif "images" == pathname.split("/")[2]:
            layout = feature_importances_images.LAYOUT
        elif "videos" == pathname.split("/")[2]:
            layout = feature_importances_videos.LAYOUT

    elif "correlation_between" == pathname.split("/")[1]:
        layout = correlation_between.LAYOUT

    elif "genetics" == pathname.split("/")[1]:
        if "gwas" == pathname.split("/")[2]:
            layout = genetics_gwas.LAYOUT
        elif "correlations" == pathname.split("/")[2]:
            layout = genetics_correlations.LAYOUT
        elif "heritability" == pathname.split("/")[2]:
            layout = genetics_heritability.LAYOUT

    elif "xwas" == pathname.split("/")[1]:
        if "univariate_results" == pathname.split("/")[2]:
            layout = xwas_univariate_results.LAYOUT
        elif "univariate_correlations" == pathname.split("/")[2]:
            layout = xwas_univariate_correlations.LAYOUT
        elif "multivariate_results" == pathname.split("/")[2]:
            layout = xwas_multivariate_results.LAYOUT
        elif "multivariate_correlations" == pathname.split("/")[2]:
            layout = xwas_multivariate_correlations.LAYOUT
        elif "multivariate_feature_importances" == pathname.split("/")[2]:
            layout = xwas_multivariate_feature_importances.LAYOUT

    elif "correlations_comparison" == pathname.split("/")[1]:
        layout = correlations_comparison.LAYOUT

    elif "/" == pathname:
        layout = introduction.LAYOUT

    else:
        layout = "404"

    return layout


@APP.callback(
    [
        Output("introduction", "active"),
        Output("datasets_scalars", "active"),
        Output("datasets_time_series", "active"),
        Output("datasets_images", "active"),
        Output("datasets_videos", "active"),
        Output("age_prediction_performances", "active"),
        Output("feature_importances_scalars", "active"),
        Output("feature_importances_time_series", "active"),
        Output("feature_importances_images", "active"),
        Output("feature_importances_videos", "active"),
        Output("correlation_between", "active"),
        Output("genetics_gwas", "active"),
        Output("genetics_heritability", "active"),
        Output("genetics_correlations", "active"),
        Output("xwas_univariate_results", "active"),
        Output("xwas_univariate_correlations", "active"),
        Output("xwas_multivariate_results", "active"),
        Output("xwas_multivariate_correlations", "active"),
        Output("xwas_multivariate_feature_importances", "active"),
        Output("correlations_comparison", "active"),
    ],
    Input("url", "pathname"),
)
def _change_active_page(pathname):
    active_pages = [False] * 20

    if "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            active_pages[1] = True
        elif "time_series" == pathname.split("/")[2]:
            active_pages[2] = True
        elif "images" == pathname.split("/")[2]:
            active_pages[3] = True
        elif "videos" == pathname.split("/")[2]:
            active_pages[4] = True

    elif "age_prediction_performances" == pathname.split("/")[1]:
        active_pages[5] = True

    elif "feature_importances" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            active_pages[6] = True
        elif "time_series" == pathname.split("/")[2]:
            active_pages[7] = True
        elif "images" == pathname.split("/")[2]:
            active_pages[8] = True
        elif "videos" == pathname.split("/")[2]:
            active_pages[9] = True

    elif "correlation_between" == pathname.split("/")[1]:
        active_pages[10] = True

    elif "genetics" == pathname.split("/")[1]:
        if "gwas" == pathname.split("/")[2]:
            active_pages[11] = True
        elif "heritability" == pathname.split("/")[2]:
            active_pages[12] = True
        elif "correlations" == pathname.split("/")[2]:
            active_pages[13] = True

    elif "xwas" == pathname.split("/")[1]:
        if "univariate_results" == pathname.split("/")[2]:
            active_pages[14] = True
        elif "univariate_correlations" == pathname.split("/")[2]:
            active_pages[15] = True
        elif "multivariate_results" == pathname.split("/")[2]:
            active_pages[16] = True
        elif "multivariate_correlations" == pathname.split("/")[2]:
            active_pages[17] = True
        elif "multivariate_feature_importances" == pathname.split("/")[2]:
            active_pages[18] = True

    elif "correlations_comparison" == pathname.split("/")[1]:
        active_pages[19] = True

    elif "/" == pathname:
        active_pages[0] = True

    return active_pages
