from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.utils.aws_loader import load_src_image
from dash_website.utils.controls import get_drop_down
from dash_website import RENAME_DIMENSIONS, DIMENSIONS_SUBDIMENSIONS
from dash_website.genetics.gwas_tabs import DIMENSIONS_TO_DROP_MANHATTAN_QQ


def get_manhattan_qq():
    return dbc.Container(
        [
            html.H1("Associations - GWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col([get_controls_manhattan_qq_gwas(), html.Br(), html.Br()], width={"size": 3})),
            dbc.Row([html.H2("Manhattan plot"), dcc.Loading(id="image_manhattan_gwas")], justify="center"),
            dbc.Row([html.H2("QQ plot"), dcc.Loading(id="image_qq_gwas")], justify="center"),
        ],
        fluid=True,
    )


def get_controls_manhattan_qq_gwas():
    dimensions_subdimensions = DIMENSIONS_SUBDIMENSIONS.copy()

    for dimension_subdimension in DIMENSIONS_TO_DROP_MANHATTAN_QQ:
        del dimensions_subdimensions[dimension_subdimension]

    return dbc.Card(
        get_drop_down("dimension_subdimension_manhattan_qq_gwas", dimensions_subdimensions, "Select a dimension:")
    )


@APP.callback(
    [Output("image_manhattan_gwas", "children"), Output("image_qq_gwas", "children")],
    Input("dimension_subdimension_manhattan_qq_gwas", "value"),
)
def _display_image_(dimension_subdimension):
    plots = []

    for plot in ["manhattan", "qq"]:
        path_to_plot = (
            f"genetics/gwas/{plot}/{RENAME_DIMENSIONS.get(dimension_subdimension, dimension_subdimension)}.png"
        )
        if plot == "manhattan":
            style = {"height": "100%", "width": "100%"}
        else:  # plot == "qq"
            style = {"height": "80%", "width": "80%", "margin-left": "10%"}

        plots.append(
            html.Img(
                src=load_src_image(path_to_plot),
                style=style,
            )
        )

    return plots
