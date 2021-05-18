from typing import Text
from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash
from dash.dependencies import Input, Output

from dash_website.utils.aws_loader import load_src_image
from dash_website.introduction.texts.introduction_text import TEXT


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


LAYOUT = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    html.Div([html.Br(), html.Br()]),
                ),
                dbc.Row(
                    dbc.Col(
                        html.H1("Multi-Dimensionality of Aging", style={"padding-top": "100px"}),
                        style={"width": 4, "text-align": "center"},
                    ),
                    className="mb-4",
                ),
                dbc.Row(
                    dbc.Col(
                        html.H6(
                            [
                                "You can ask us some questions, report some errors or give us some feedback ",
                                html.A(
                                    "here",
                                    href="https://github.com/Deep-Learning-and-Aging/Website/discussions",
                                ),
                                ".",
                            ],
                            style={"padding-top": "100px"},
                        ),
                        style={"text-align": "center"},
                    ),
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
                dbc.Row(
                    dbc.Col(
                        [
                            html.Img(
                                src=load_src_image("introduction/logo_harvard.png"),
                                style={"height": 200, "margin-left": "600px"},
                            ),
                            html.Img(
                                src=load_src_image("introduction/logo_hms.png"),
                                style={"height": 200, "float": "right", "margin-right": "600px"},
                            ),
                        ],
                    ),
                    justify="center",
                ),
            ],
            style={"padding-bottom": 100},
        ),
        html.Div(
            [
                html.H4(
                    [
                        html.A(
                            "Alan Le Goallec",
                            href="https://www.linkedin.com/in/alan-le-goallec-1990/",
                            style={"color": "white"},
                        ),
                        html.Sup("1, 2"),
                        ", ",
                        html.A(
                            "Sasha Collin",
                            href="https://www.linkedin.com/in/sasha-collin-a2941115b/",
                            style={"color": "white"},
                        ),
                        html.Sup("1+"),
                        ", ",
                        html.A(
                            "Samuel Diai",
                            href="https://www.linkedin.com/in/samueldiai/",
                            style={"color": "white"},
                        ),
                        html.Sup("1+"),
                        ", ",
                        html.A(
                            "Jean-Baptiste Prost",
                            href="https://www.linkedin.com/in/jbprost/",
                            style={"color": "white"},
                        ),
                        html.Sup("1"),
                        ", ",
                        html.A(
                            "M’Hamed Jabri",
                            href="https://www.linkedin.com/in/mhamed-jabri/",
                            style={"color": "white"},
                        ),
                        html.Sup("1"),
                        ", ",
                        html.A(
                            "Théo Vincent",
                            href="https://www.linkedin.com/in/theo-vincent/",
                            style={"color": "white"},
                        ),
                        html.Sup("1"),
                        " and ",
                        html.A(
                            "Chirag J. Patel",
                            href="https://www.linkedin.com/in/chirag-j-patel/",
                            style={"color": "white"},
                        ),
                        html.Sup("1*"),
                    ],
                    style={"font-size": "18px"},
                ),
                html.H5(
                    [
                        html.Sup("1"),
                        html.A(
                            "Department of Biomedical Informatics, Harvard Medical School, Boston, MA, 02115, USA",
                            href="https://dbmi.hms.harvard.edu/",
                            style={"color": "white"},
                        ),
                        ", ",
                        html.Sup("2"),
                        html.A(
                            "Department of Systems, Synthetic and Quantitative Biology, Harvard University, Cambridge, MA, 02118, USA",
                            href="https://sysbio.med.harvard.edu/",
                            style={"color": "white"},
                        ),
                        ", ",
                        html.Sup("+"),
                        "Co-second authors, ",
                        html.Sup("*"),
                        "Corresponding author",
                    ],
                    style={"font-size": "13px"},
                ),
            ],
            style={
                "position": "fixed",
                "bottom": 0,
                "width": "100%",
                "background": "#0070FF",
                "line-height": 2,
                "text-align": "center",
                "color": "white",
                "Font-size": 14,
                "font-weight": "bold",
                "text-shadow": "0 1px 0 #84BAFF",
                "box-shadow": "0 0 15px #00214B",
                "padding-top": 15,
                "padding-bottom": 15,
            },
        ),
    ]
)
