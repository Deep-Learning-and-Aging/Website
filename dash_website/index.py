import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from dash_website.app import APP
from dash_website.utils.aws_loader import load_src_image

# IMPORT LAYOUTS
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


# IMPORT INFORMATION
import dash_website.texts.datasets.scalars as info_datasets_scalars
import dash_website.texts.datasets.time_series as info_datasets_time_series
import dash_website.texts.datasets.images as info_datasets_images
import dash_website.texts.datasets.videos as info_datasets_videos

import dash_website.texts.age_prediction_performances.age_prediction_performances as info_age_prediction_performances

import dash_website.texts.feature_importances.scalars as info_feature_importances_scalars
import dash_website.texts.feature_importances.time_series as info_feature_importances_time_series
import dash_website.texts.feature_importances.images as info_feature_importances_images
import dash_website.texts.feature_importances.videos as info_feature_importances_videos

import dash_website.texts.correlation_between.correlation_between as info_correlation_between

import dash_website.texts.genetics.gwas as info_genetics_gwas
import dash_website.texts.genetics.correlations as info_genetics_correlations
import dash_website.texts.genetics.heritability as info_genetics_heritability

import dash_website.texts.xwas.univariate_results as info_xwas_univariate_results
import dash_website.texts.xwas.univariate_correlations as info_xwas_univariate_correlations
import dash_website.texts.xwas.multivariate_results as info_xwas_multivariate_results
import dash_website.texts.xwas.multivariate_correlations as info_xwas_multivariate_correlations
import dash_website.texts.xwas.multivariate_feature_importances as info_xwas_multivariate_feature_importances

import dash_website.texts.correlations_comparison.correlations_comparison as info_correlations_comparison


def get_server():
    add_layout(APP)
    return APP.server


def launch_local_website():
    add_layout(APP)
    APP.run_server(debug=True)


def add_layout(app):
    app.layout = html.Div(
        [
            html.Div(id="blank-output"),
            dcc.Location(id="url", refresh=False),
            get_top_bar(),
            html.Hr(),
            html.Div(id="page_content"),
            html.Div(
                [
                    dbc.Button(
                        html.Img(src=load_src_image("info_icon.png"), style={"height": "100%", "width": "100%"}),
                        id="open_info",
                        color="transparent",
                    ),
                    dbc.Modal(
                        [
                            dbc.ModalHeader("Age prediction performances", id="info_header"),
                            dbc.ModalBody("This modal is vertically centered", id="info_text"),
                            dbc.ModalFooter(dbc.Button("Close", id="close_info", className="ml-auto")),
                        ],
                        id="info",
                        backdrop=False,
                        centered=True,
                        scrollable=True,
                        size="xl",
                    ),
                ],
                id="div_info",
                style={"display": "None"},
            ),
        ],
        style={"height": "100vh", "fontSize": 14},
    )


def get_top_bar():
    return html.Div(
        [
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Introduction", href="/", active=True, id="introduction")),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Phenotypic",
                                href="/correlation_between_aging_dimensions/phenotypic",
                                id="correlation_between_aging_dimensions_phenotypic",
                            ),
                            dbc.DropdownMenuItem(
                                "Genetics",
                                href="/correlation_between_aging_dimensions/genetics",
                                id="correlation_between_aging_dimensions_genetics",
                            ),
                            dbc.DropdownMenuItem(
                                "XWAS - Univariate",
                                href="/correlation_between_aging_dimensions/xwas_univariate",
                                id="correlation_between_aging_dimensions_xwas_univariate",
                            ),
                            dbc.DropdownMenuItem(
                                "XWAS - Multivariate",
                                href="/correlation_between_aging_dimensions/xwas_multivariate",
                                id="correlation_between_aging_dimensions_xwas_multivariate",
                            ),
                            dbc.DropdownMenuItem(
                                "Comparison",
                                href="/correlation_between_aging_dimensions/comparison",
                                id="correlation_between_aging_dimensions_comparison",
                            ),
                        ],
                        label="Correlation between aging dimensions",
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
                                "Scalars", href="/model_interpretability/scalars", id="model_interpretability_scalars"
                            ),
                            dbc.DropdownMenuItem(
                                "Time Series",
                                href="/model_interpretability/time_series",
                                id="model_interpretability_time_series",
                            ),
                            dbc.DropdownMenuItem(
                                "Images", href="/model_interpretability/images", id="model_interpretability_images"
                            ),
                            dbc.DropdownMenuItem(
                                "Videos", href="/model_interpretability/videos", id="model_interpretability_videos"
                            ),
                        ],
                        label="Model interpretability",
                        nav=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem("Associations", href="/gwas/associations", id="gwas_associations"),
                            dbc.DropdownMenuItem("Heritability", href="/gwas/heritability", id="gwas_heritability"),
                        ],
                        label="GWAS",
                        nav=True,
                    ),
                    dbc.DropdownMenu(
                        [
                            dbc.DropdownMenuItem(
                                "Univariate associations",
                                href="/xwas/univariate_associations",
                                id="xwas_univariate_associations",
                            ),
                            dbc.DropdownMenuItem(
                                "Accelerated aging prediction - Performance",
                                href="/xwas/accelerated_aging_prediction_performance",
                                id="xwas_accelerated_aging_prediction_performance",
                            ),
                            dbc.DropdownMenuItem(
                                "Accelerated aging prediction - Interpretability",
                                href="/xwas/accelerated_aging_prediction_interpretability",
                                id="xwas_accelerated_aging_prediction_interpretability",
                            ),
                        ],
                        label="XWAS",
                        nav=True,
                    ),
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


APP.clientside_callback(
    """
    function(pathname) {
        document.title = "Error on Multidimensionality of aging"
        if ("correlation_between_aging_dimensions" === pathname.split("/")[1]) {
            if ("phenotypic" === pathname.split("/")[2]) {
                document.title = "Phenotype correlations"
            } else if ("genetics" === pathname.split("/")[2]) {
                document.title = "Genetics correlations"
            } else if ("xwas_univariate" === pathname.split("/")[2]) {
                document.title = "XWAS univariate correlations"
            } else if ("xwas_multivariate" === pathname.split("/")[2]) {
                document.title = "XWAS multivariate correlations"
            } else if ("comparison" === pathname.split("/")[2]) {
                document.title = "Correlations comparison"
            }
        } else if ("age_prediction_performances" === pathname.split("/")[1]) {
            document.title = "Age prediction performances"
        } else if ("model_interpretability" === pathname.split("/")[1]) {
            if ("scalars" === pathname.split("/")[2]) {
                document.title = "Model interpretability scalars"
            } else if ("time_series" === pathname.split("/")[2]) {
                document.title = "Model interpretability time series"
            } else if ("images" === pathname.split("/")[2]) {
                document.title = "Model interpretability images"
            } else if ("videos" === pathname.split("/")[2]) {
                document.title = "Model interpretability videos"
            }
        } else if ("gwas" === pathname.split("/")[1]) {
            if ("associations" === pathname.split("/")[2]) {
                document.title = "GWAS associations"
            } else if ("heritability" === pathname.split("/")[2]) {
                document.title = "GWAS heritability"
            }
        } else if ("xwas" === pathname.split("/")[1]) {
            if ("univariate_associations" === pathname.split("/")[2]) {
                document.title = "XWAS univariate associations"
            } else if ("accelerated_aging_prediction_performance" === pathname.split("/")[2]) {
                document.title = "XWAS multivariate performance"
            } else if ("accelerated_aging_prediction_interpretability" === pathname.split("/")[2]) {
                document.title = "XWAS multivariate interpretability"
            }
        } else if ("datasets" === pathname.split("/")[1]) {
            if ("scalars" === pathname.split("/")[2]) {
                document.title = "Datasets scalars"
            }
            else if ("time_series" === pathname.split("/")[2]) {
                document.title = "Datasets time series"
            }
            else if ("images" === pathname.split("/")[2]) {
                document.title = "Datasets images"
            }
            else if ("videos" === pathname.split("/")[2]) {
                document.title = "Datasets videos"
            }
        } else if ("/" === pathname) {
            document.title = "Multidimensionality of aging"
        }
    }
    """,
    Output("blank-output", "children"),
    Input("url", "pathname"),
)


# THIS CALLBACK MAPS THE WEBSITE PAGE ORGANISATION TO THE CODE PAGE ORGANISATION
@APP.callback(Output("page_content", "children"), Input("url", "pathname"))
def _display_page(pathname):
    layout = "404"

    if "correlation_between_aging_dimensions" == pathname.split("/")[1]:
        if "phenotypic" == pathname.split("/")[2]:
            layout = correlation_between.LAYOUT
        elif "genetics" == pathname.split("/")[2]:
            layout = genetics_correlations.LAYOUT
        elif "xwas_univariate" == pathname.split("/")[2]:
            layout = xwas_univariate_correlations.LAYOUT
        elif "xwas_multivariate" == pathname.split("/")[2]:
            layout = xwas_multivariate_correlations.LAYOUT
        elif "comparison" == pathname.split("/")[2]:
            layout = correlations_comparison.LAYOUT

    elif "age_prediction_performances" == pathname.split("/")[1]:
        layout = age_prediction_performances.LAYOUT

    elif "model_interpretability" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            layout = feature_importances_scalars.LAYOUT
        elif "time_series" == pathname.split("/")[2]:
            layout = feature_importances_time_series.LAYOUT
        elif "images" == pathname.split("/")[2]:
            layout = feature_importances_images.LAYOUT
        elif "videos" == pathname.split("/")[2]:
            layout = feature_importances_videos.LAYOUT

    elif "gwas" == pathname.split("/")[1]:
        if "associations" == pathname.split("/")[2]:
            layout = genetics_gwas.LAYOUT
        elif "heritability" == pathname.split("/")[2]:
            layout = genetics_heritability.LAYOUT

    elif "xwas" == pathname.split("/")[1]:
        if "univariate_associations" == pathname.split("/")[2]:
            layout = xwas_univariate_results.LAYOUT
        elif "accelerated_aging_prediction_performance" == pathname.split("/")[2]:
            layout = xwas_multivariate_results.LAYOUT
        elif "accelerated_aging_prediction_interpretability" == pathname.split("/")[2]:
            layout = xwas_multivariate_feature_importances.LAYOUT

    elif "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            layout = datasets_scalars.LAYOUT
        elif "time_series" == pathname.split("/")[2]:
            layout = datasets_time_series.LAYOUT
        elif "images" == pathname.split("/")[2]:
            layout = datasets_images.LAYOUT
        elif "videos" == pathname.split("/")[2]:
            layout = datasets_videos.LAYOUT

    elif "/" == pathname:
        layout = introduction.LAYOUT

    return layout


@APP.callback(
    [
        Output("introduction", "active"),
        Output("correlation_between_aging_dimensions_phenotypic", "active"),
        Output("correlation_between_aging_dimensions_genetics", "active"),
        Output("correlation_between_aging_dimensions_xwas_univariate", "active"),
        Output("correlation_between_aging_dimensions_xwas_multivariate", "active"),
        Output("correlation_between_aging_dimensions_comparison", "active"),
        Output("age_prediction_performances", "active"),
        Output("model_interpretability_scalars", "active"),
        Output("model_interpretability_time_series", "active"),
        Output("model_interpretability_images", "active"),
        Output("model_interpretability_videos", "active"),
        Output("gwas_associations", "active"),
        Output("gwas_heritability", "active"),
        Output("xwas_univariate_associations", "active"),
        Output("xwas_accelerated_aging_prediction_performance", "active"),
        Output("xwas_accelerated_aging_prediction_interpretability", "active"),
        Output("datasets_scalars", "active"),
        Output("datasets_time_series", "active"),
        Output("datasets_images", "active"),
        Output("datasets_videos", "active"),
    ],
    Input("url", "pathname"),
)
def _change_active_page(pathname):
    active_pages = [False] * 20

    if "correlation_between_aging_dimensions" == pathname.split("/")[1]:
        if "phenotypic" == pathname.split("/")[2]:
            active_pages[1] = True
        elif "genetics" == pathname.split("/")[2]:
            active_pages[2] = True
        elif "xwas_univariate" == pathname.split("/")[2]:
            active_pages[3] = True
        elif "xwas_multivariate" == pathname.split("/")[2]:
            active_pages[4] = True
        elif "comparison" == pathname.split("/")[2]:
            active_pages[5] = True

    elif "age_prediction_performances" == pathname.split("/")[1]:
        active_pages[6] = True

    elif "model_interpretability" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            active_pages[7] = True
        elif "time_series" == pathname.split("/")[2]:
            active_pages[8] = True
        elif "images" == pathname.split("/")[2]:
            active_pages[9] = True
        elif "videos" == pathname.split("/")[2]:
            active_pages[10] = True

    elif "gwas" == pathname.split("/")[1]:
        if "associations" == pathname.split("/")[2]:
            active_pages[11] = True
        elif "heritability" == pathname.split("/")[2]:
            active_pages[12] = True

    elif "xwas" == pathname.split("/")[1]:
        if "xwas_univariate_associations" == pathname.split("/")[2]:
            active_pages[13] = True
        elif "xwas_accelerated_aging_prediction_performance" == pathname.split("/")[2]:
            active_pages[14] = True
        elif "xwas_accelerated_aging_prediction_interpretability" == pathname.split("/")[2]:
            active_pages[15] = True

    elif "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            active_pages[16] = True

        elif "time_series" == pathname.split("/")[2]:
            active_pages[17] = True
        elif "images" == pathname.split("/")[2]:
            active_pages[18] = True
        elif "videos" == pathname.split("/")[2]:
            active_pages[19] = True

    elif "/" == pathname:
        active_pages[0] = True

    return active_pages


@APP.callback(Output("div_info", component_property="style"), Input("url", "pathname"))
def _display_div_info(pathname):
    if "/" == pathname:
        return {"display": "None"}
    else:
        return {
            "position": "fixed",
            "bottom": 0,
            "left": 40,
            "width": "5%",
            "background": "#0070FF",
            "text-align": "center",
            "box-shadow": "0 0 15px #00214B",
        }


@APP.callback(
    Output("info", "is_open"),
    [Input("open_info", "n_clicks"), Input("close_info", "n_clicks")],
    State("info", "is_open"),
)
def _toggle_modal(open_button_clicks, close_button_clicks, is_open):
    if open_button_clicks or close_button_clicks:
        return not is_open
    return is_open


@APP.callback([Output("info_header", "children"), Output("info_text", "children")], Input("url", "pathname"))
def _fill_info(pathname):
    header, text = None, None

    if "correlation_between_aging_dimensions" == pathname.split("/")[1]:
        if "phenotypic" == pathname.split("/")[2]:
            header = "Correlation between aging dimensions - Phenotypic"
            text = info_correlation_between.TEXT
        elif "genetics" == pathname.split("/")[2]:
            header = "Correlation between aging dimensions - Genetics"
            text = info_genetics_correlations.TEXT
        elif "xwas_univariate" == pathname.split("/")[2]:
            header = "Correlation between aging dimensions - XWAS Univariate"
            text = info_xwas_univariate_correlations.TEXT
        elif "xwas_multivariate" == pathname.split("/")[2]:
            header = "Correlation between aging dimensions - XWAS Multivariate"
            text = info_xwas_multivariate_correlations.TEXT
        elif "comparison" == pathname.split("/")[2]:
            header = "Correlation between aging dimensions - Comparison"
            text = info_correlations_comparison.TEXT

    elif "age_prediction_performances" == pathname.split("/")[1]:
        header = "Age prediction performances"
        text = info_age_prediction_performances.TEXT

    elif "model_interpretability" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            header = "Model interpretability - Scalars"
            text = info_feature_importances_scalars.TEXT
        elif "time_series" == pathname.split("/")[2]:
            header = "Model interpretability - Time series"
            text = info_feature_importances_time_series.TEXT
        elif "images" == pathname.split("/")[2]:
            header = "Model interpretability - Images"
            text = info_feature_importances_images.TEXT
        elif "videos" == pathname.split("/")[2]:
            header = "Model interpretability - Videos"
            text = info_feature_importances_videos.TEXT

    elif "gwas" == pathname.split("/")[1]:
        if "associations" == pathname.split("/")[2]:
            header = "GWAS - Associations"
            text = info_genetics_gwas.TEXT
        elif "heritability" == pathname.split("/")[2]:
            header = "GWAS - Heritability"
            text = info_genetics_heritability.TEXT

    elif "xwas" == pathname.split("/")[1]:
        if "univariate_associations" == pathname.split("/")[2]:
            header = "XWAS - Univariate associations"
            text = info_xwas_univariate_results.TEXT
        elif "accelerated_aging_prediction_performance" == pathname.split("/")[2]:
            header = "XWAS - Accelerated aging prediction - Performance"
            text = info_xwas_multivariate_results.TEXT
        elif "accelerated_aging_prediction_interpretability" == pathname.split("/")[2]:
            header = "XWAS - Accelerated aging prediction - Interpretability"
            text = info_xwas_multivariate_feature_importances.TEXT

    elif "datasets" == pathname.split("/")[1]:
        if "scalars" == pathname.split("/")[2]:
            header = "Datasets - Scalars"
            text = info_datasets_scalars.TEXT
        elif "time_series" == pathname.split("/")[2]:
            header = "Datasets - Time series"
            text = info_datasets_time_series.TEXT
        elif "images" == pathname.split("/")[2]:
            header = "Datasets - Images"
            text = info_datasets_images.TEXT
        elif "videos" == pathname.split("/")[2]:
            header = "Datasets - Videos"
            text = info_datasets_videos.TEXT

    return header, text
