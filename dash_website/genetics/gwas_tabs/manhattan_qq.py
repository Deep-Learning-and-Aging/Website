from os import path
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_src_image
from dash_website.utils.controls import get_drop_down
from dash_website.genetics import DIMENSIONS_GWAS


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
    return dbc.Card(
        get_drop_down("dimensions_manhattan_qq_gwas", DIMENSIONS_GWAS, "Select a dimension:", from_dict=False)
    )


@APP.callback(
    [Output("image_manhattan_gwas", "children"), Output("image_qq_gwas", "children")],
    Input("dimensions_manhattan_qq_gwas", "value"),
)
def _display_image_(dimension):
    plots = []

    for plot in ["manhattan", "qq"]:
        path_to_plot = f"genetics/gwas/{plot}/{dimension}.png"
        if plot == "manhattan":
            style = {"height": 900, "padding-top": "100px"}
        else:  # plot == "qq"
            style = {"width": 1000}

        plots.append(
            html.Img(
                src=load_src_image(path_to_plot),
                style=style,
            )
        )

    return plots
