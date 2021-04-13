from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output, State

from dash_website.introduction.cards import standard_card, faded_card


def get_layout():
    return html.Div(
        [
            dbc.Row(
                dbc.Col(html.H1("Multi-Dimensionality of Aging", id="kk"), width={"size": True, "offset": 4}),
                className="mb-4",
            ),
            dbc.Row(
                [
                    standard_card("introduction_button", "Introduction", "primary"),
                    standard_card("datasets_button", "Datasets", "secondary"),
                    standard_card("age_prediction_performances_button", "Age prediction performances", "info"),
                    standard_card("feature_importances_button", "Feature importances", "secondary"),
                    standard_card("correlation_button", "Correlation between accelerated aging and dimensions", "info"),
                    standard_card("genetics_button", "Genetics", "secondary"),
                    standard_card("xwas_button", "XWAS", "info"),
                ],
                className="mb-4",
                no_gutters=False,
            ),
            dbc.Row(
                [
                    faded_card("faded_introduction", "!!!!!This content fades in and out!!!!!", is_in=True),
                    faded_card("faded_datasets", "This content fades in and out"),
                    faded_card("faded_age_prediction_performances", "This content fades in and out"),
                    faded_card("faded_feature_importances", "This content fades in and out"),
                    faded_card("faded_correlation", "This content fades in and out"),
                    faded_card("faded_genetics", "This content fades in and out"),
                    faded_card("faded_xwas", "This content fades in and out"),
                ],
                className="mb-4",
            ),
        ],
        id="id_menu",
    )


@APP.callback(
    [
        Output("faded_introduction", "is_in"),
        Output("faded_datasets", "is_in"),
        Output("faded_age_prediction_performances", "is_in"),
        Output("faded_feature_importances", "is_in"),
        Output("faded_correlation", "is_in"),
        Output("faded_genetics", "is_in"),
        Output("faded_xwas", "is_in"),
    ],
    [
        Input("introduction_button", "n_clicks"),
        Input("datasets_button", "n_clicks"),
        Input("age_prediction_performances_button", "n_clicks"),
        Input("feature_importances_button", "n_clicks"),
        Input("correlation_button", "n_clicks"),
        Input("genetics_button", "n_clicks"),
        Input("xwas_button", "n_clicks"),
    ],
    [
        State("faded_introduction", "is_in"),
        State("faded_datasets", "is_in"),
        State("faded_age_prediction_performances", "is_in"),
        State("faded_feature_importances", "is_in"),
        State("faded_correlation", "is_in"),
        State("faded_genetics", "is_in"),
        State("faded_xwas", "is_in"),
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
    is_in_introduction,
    is_in_datasets,
    is_in_age_prediction_performances,
    is_in_feature_importances,
    is_in_correlation,
    is_in_genetics,
    is_in_xwas,
):
    clicked_card = dash.callback_context.triggered[0]["prop_id"].split(".")[0]

    if clicked_card == "introduction_button":
        return [not is_in_introduction, False, False, False, False, False, False]
    elif clicked_card == "datasets_button":
        return [False, not is_in_datasets, False, False, False, False, False]
    elif clicked_card == "age_prediction_performances_button":
        return [False, False, not is_in_age_prediction_performances, False, False, False, False]
    elif clicked_card == "feature_importances_button":
        return [False, False, False, not is_in_feature_importances, False, False, False]
    elif clicked_card == "correlation_button":
        return [False, False, False, False, not is_in_correlation, False, False]
    elif clicked_card == "genetics_button":
        return [False, False, False, False, False, not is_in_genetics, False]
    elif clicked_card == "xwas_button":
        return [False, False, False, False, False, False, not is_in_xwas]
    else:
        return [is_in_introduction, False, False, False, False, False, False]
