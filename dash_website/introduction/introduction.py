from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

from dash_website.introduction.cards import standard_card
from dash_website import COLORS_SECTIONS


def get_layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(html.H1("Multi-Dimensionality of Aging", id="kk"), width={"size": True, "offset": 4}),
                className="mb-4",
            ),
            dbc.Row(
                [
                    standard_card("introduction_button", "Introduction", COLORS_SECTIONS["introduction"]),
                    standard_card("datasets_button", "Datasets", COLORS_SECTIONS["datasets"]),
                    standard_card(
                        "age_prediction_performances_button",
                        "Age prediction performances",
                        COLORS_SECTIONS["age_prediction_performances"],
                    ),
                    standard_card(
                        "feature_importances_button", "Feature importances", COLORS_SECTIONS["feature_importances"]
                    ),
                    standard_card(
                        "correlation_button",
                        "Correlation between accelerated aging and dimensions",
                        COLORS_SECTIONS["correlation"],
                    ),
                    standard_card("genetics_button", "Genetics", COLORS_SECTIONS["genetics"]),
                    standard_card("xwas_button", "XWAS", COLORS_SECTIONS["xwas"]),
                ],
                className="mb-4",
                no_gutters=False,
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Card(
                        html.P(id="core_card_text", className="card-text"),
                        id="core_card",
                        color="primary",
                        outline=True,
                    ),
                    width=8,
                ),
                justify="center",
            ),
        ],
        id="id_menu",
    )


@APP.callback(
    [Output("core_card_text", "children"), Output("core_card", "color")],
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
    clicked_card = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if clicked_card == "introduction_button":
        from dash_website.introduction.texts.introduction_text import get_text_color
    elif clicked_card == "datasets_button":
        from dash_website.introduction.texts.datasets_text import get_text_color
    elif clicked_card == "age_prediction_performances_button":
        from dash_website.introduction.texts.age_prediction_performances_text import get_text_color
    elif clicked_card == "feature_importances_button":
        from dash_website.introduction.texts.feature_importances_text import get_text_color
    elif clicked_card == "correlation_button":
        from dash_website.introduction.texts.correlation_text import get_text_color
    elif clicked_card == "genetics_button":
        from dash_website.introduction.texts.genetics_text import get_text_color
    elif clicked_card == "xwas_button":
        from dash_website.introduction.texts.xwas_text import get_text_color
    else:
        from dash_website.introduction.texts.introduction_text import get_text_color

    return get_text_color()