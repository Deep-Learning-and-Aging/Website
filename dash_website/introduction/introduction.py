from typing import Text
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

from dash_website.introduction.texts.introduction_text import TEXT


def get_layout():
    return html.Div(
        [
            dbc.Row(
                html.Div([html.Br(), html.Br()]),
            ),
            dbc.Row(
                [
                    dbc.Col(html.H1("Multi-Dimensionality of Aging", id="kk"), width={"size": True, "offset": 4}),
                ],
                className="mb-4",
            ),
            dbc.Row(
                html.Div([html.Br(), html.Br()]),
            ),
            dbc.Row(
                [
                    standard_button("introduction_button", "Introduction"),
                    standard_button("datasets_button", "Datasets"),
                    standard_button("age_prediction_performances_button", "Age prediction performances"),
                    standard_button("feature_importances_button", "Feature importances"),
                    standard_button("correlation_button", "Correlation between accelerated aging and dimensions"),
                    standard_button("genetics_button", "Genetics"),
                    standard_button("xwas_button", "XWAS"),
                ],
                className="mb-4",
                no_gutters=False,
            ),
            dbc.Row(
                html.Div([html.Br(), html.Br()]),
            ),
            dbc.Row(dbc.Col(id="core_div", children=TEXT, width=8), justify="center"),
        ],
        id="id_menu",
    )


def standard_button(id, name):
    return dbc.Col(dbc.Button(name, id=id, color="Transparent", block=True))


@APP.callback(
    Output("core_div", "children"),
    [
        Input("introduction_button", "n_clicks"),
        Input("datasets_button", "n_clicks"),
        Input("age_prediction_performances_button", "n_clicks"),
        Input("feature_importances_button", "n_clicks"),
        Input("correlation_button", "n_clicks"),
        Input("genetics_button", "n_clicks"),
        Input("xwas_button", "n_clicks"),
    ],
)
def _toggle_fade(
    n_clicks_introduction,
    n_clicks_datasets,
    n_clicks_age_prediction_performances,
    n_clicks_feature_importances,
    n_clicks_correlation,
    n_clicks_genetics,
    n_clicks_xwas,
):
    clicked_button = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if clicked_button == "introduction_button":
        from dash_website.introduction.texts.introduction_text import TEXT
    elif clicked_button == "datasets_button":
        from dash_website.introduction.texts.datasets_text import TEXT
    elif clicked_button == "age_prediction_performances_button":
        from dash_website.introduction.texts.age_prediction_performances_text import TEXT
    elif clicked_button == "feature_importances_button":
        from dash_website.introduction.texts.feature_importances_text import TEXT
    elif clicked_button == "correlation_button":
        from dash_website.introduction.texts.correlation_text import TEXT
    elif clicked_button == "genetics_button":
        from dash_website.introduction.texts.genetics_text import TEXT
    elif clicked_button == "xwas_button":
        from dash_website.introduction.texts.xwas_text import TEXT
    else:
        from dash_website.introduction.texts.introduction_text import TEXT

    return TEXT