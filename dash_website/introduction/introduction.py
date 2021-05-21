import dash_bootstrap_components as dbc
import dash_html_components as html

from dash_website.utils.aws_loader import load_src_image
import dash_website.texts.introduction.introduction as info_introduction


LAYOUT = html.Div(
    [
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.H1("Multidimensionality of Aging", style={"padding-top": "50px"}),
                        style={"width": 4, "text-align": "center"},
                    ),
                    className="mb-4",
                ),
                dbc.Row(
                    dbc.Col(
                        html.H6(
                            [
                                "Feel free to report errors, provide feedback or ask questions about our work ",
                                html.A(
                                    "here",
                                    href="https://github.com/Deep-Learning-and-Aging/Website/discussions",
                                ),
                                ".",
                            ],
                            style={"padding-top": "50px"},
                        ),
                        style={"text-align": "center"},
                    ),
                ),
                dbc.Row(
                    dbc.Col(info_introduction.TEXT, width=8),
                    justify="center",
                    style={"padding-top": "20px"},
                ),
                html.Div(
                    [
                        html.Img(
                            src=load_src_image("introduction/logo_harvard.png"),
                            style={"height": "10%", "width": "10%", "margin-left": "25%"},
                        ),
                        html.Img(
                            src=load_src_image("introduction/logo_hms.png"),
                            style={"height": "8%", "width": "8%", "float": "right", "margin-right": "25%"},
                        ),
                    ]
                ),
                html.Div([html.Br(), html.Br()]),
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
                    style={"font-size": "22px"},
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
                    style={"font-size": "16px"},
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
