import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, load_csv
from plotly.graph_objs import Scattergl, Scatter, Histogram, Figure, Bar
from plotly.subplots import make_subplots
from dash_website.app import APP, MODE
import numpy as np

distinct_colors = [
    "#e6194b",
    "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#46f0f0",
    "#f032e6",
    "#bcf60c",
    "#fabebe",
    "#008080",
    "#e6beff",
    "#9a6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#000075",
    "#808080",
    "#ffffff",
    "#000000",
]

path_performance = "page2_predictions/Performances/"
organs = [
    "*",
    "*instances23",
    "*instances1.5x",
    "*instances01",
    "Abdomen",
    "Arterial",
    "Biochemistry",
    "Brain",
    "Eyes",
    "Hearing",
    "Heart",
    "ImmuneSystem",
    "Lungs",
    "Musculoskeletal",
    "PhysicalActivity",
]
value_step = "Test"


if MODE != "All":
    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances",
                        options=[{"value": "eids", "label": "Individuals"}, {"value": "instances", "label": "Samples"}],
                        value="instances",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select aggregate type : "),
                    dcc.RadioItems(
                        id="select_aggregate_type",
                        options=[
                            {"value": "withEnsembles", "label": "All models"},
                            {"value": "tuned", "label": "Non-ensemble models"},
                        ],
                        value="withEnsembles",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(id="Select_organ", options=get_dataset_options([MODE]), value=MODE),
                    html.Br(),
                ],
                style={"display": "none"},
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step',
            #         options = get_dataset_options(['Train', 'Test', 'Validation']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ]),
            dbc.FormGroup(
                [
                    html.P("Select a scoring metric : "),
                    dcc.RadioItems(
                        id="Select_metric",
                        options=get_dataset_options(["RMSE", "R2"]),
                        value="R2",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
        ]
    )

else:
    controls = dbc.Card(
        [
            dbc.FormGroup(
                [
                    html.P("Select eid vs instances : "),
                    dcc.RadioItems(
                        id="select_eid_or_instances",
                        options=[{"value": "eids", "label": "Individuals"}, {"value": "instances", "label": "Samples"}],
                        value="instances",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select which models to display : "),
                    dcc.RadioItems(
                        id="select_aggregate_type",
                        options=[
                            {"value": "bestmodels", "label": "Best models"},
                            {"value": "withEnsembles", "label": "All models"},
                            {"value": "tuned", "label": "Non-ensemble models"},
                        ],
                        value="bestmodels",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
            dbc.FormGroup(
                [
                    html.P("Select an Organ : "),
                    dcc.Dropdown(
                        id="Select_organ", options=get_dataset_options(organs + ["All"]), placeholder="All", value="All"
                    ),
                    html.Br(),
                ]
            ),
            # dbc.FormGroup([
            #     html.P("Select step : "),
            #     dcc.Dropdown(
            #         id='Select_step',
            #         options = get_dataset_options(['Train', 'Test', 'Validation']),
            #         value = 'Test'
            #         ),
            #     html.Br()
            # ]),
            dbc.FormGroup(
                [
                    html.P("Select a scoring metric : "),
                    dcc.RadioItems(
                        id="Select_metric",
                        options=get_dataset_options(["RMSE", "R2"]),
                        value="R2",
                        labelStyle={"display": "inline-block", "margin": "5px"},
                    ),
                    html.Br(),
                ]
            ),
        ]
    )


layout = dbc.Container(
    [
        html.H1("Age prediction performances"),
        html.Br(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col([controls, html.Br(), html.Br()], md=3),
                dbc.Col(
                    [
                        dcc.Graph(id="Plot R2 scores"),
                    ],
                    style={"overflowY": "scroll", "height": 600, "overflowX": "scroll", "width": 700},
                    md=9,
                ),
            ]
        ),
    ],
    fluid=True,
)


@APP.callback(
    Output("Plot R2 scores", "figure"),
    [
        Input("select_eid_or_instances", "value"),
        Input("select_aggregate_type", "value"),
        Input("Select_organ", "value"),
        # Input('Select_step', 'value'),
        Input("Select_metric", "value"),
    ],
)
def _plot_r2_scores(
    value_eid_vs_instances,
    value_aggregate,
    value_organ,
    # value_step,
    value_metric,
):
    if value_metric == "R2":
        metric = "R-Squared_all"
        std = "R-Squared_sd_all"
    elif value_metric == "RMSE":
        metric = "RMSE_all"
        std = "RMSE_sd_all"

    else:
        raise ValueError("WRONG METRIC ! ")
    if value_step == "Validation":
        df = load_csv(
            path_performance + "PERFORMANCES_%s_ranked_%s_Age_val.csv" % (value_aggregate, value_eid_vs_instances)
        )
        df_res = df[
            [
                "target",
                "organ",
                "view",
                "transformation",
                "architecture",
                "RMSE_all",
                "RMSE_sd_all",
                "R-Squared_all",
                "R-Squared_sd_all",
                "N_all",
            ]
        ]
        df_res = df_res.sort_values(["organ", "view", "transformation", "architecture"])

    elif value_step == "Train":
        df = load_csv(
            path_performance + "PERFORMANCES_%s_ranked_%s_Age_train.csv" % (value_aggregate, value_eid_vs_instances)
        )
        df_res = df[
            [
                "target",
                "organ",
                "view",
                "transformation",
                "architecture",
                "RMSE_all",
                "RMSE_sd_all",
                "R-Squared_all",
                "R-Squared_sd_all",
                "N_all",
            ]
        ]
        df_res = df_res.sort_values(["organ", "view", "transformation", "architecture"])

    elif value_step == "Test":
        df = load_csv(
            path_performance + "PERFORMANCES_%s_ranked_%s_Age_test.csv" % (value_aggregate, value_eid_vs_instances)
        )
        df_res = df[
            [
                "target",
                "organ",
                "view",
                "transformation",
                "architecture",
                "RMSE_all",
                "RMSE_sd_all",
                "R-Squared_all",
                "R-Squared_sd_all",
                "N_all",
            ]
        ]
        df_res = df_res.sort_values(["organ", "view", "transformation", "architecture"])

    if value_aggregate == "bestmodels" and value_organ == "All":
        df_res["view"] = df_res["view"].str.replace("*", "")
        df_res["organ"] = [organ + view for organ, view in zip(df_res["organ"], df_res["view"])]
        d = {
            "data": Bar(
                x=df_res["organ"].values,
                y=df_res[metric],
                hovertemplate="Organ : %{x}\
                                              <br>Score : %{y}\
                                              <br>Sample Size : %{customdata}",
                customdata=df_res["N_all"],
                error_y=dict(type="data", array=df_res[std]),
            ),
            "layout": dict(
                height=600,
                width=max(20 * len(df_res["architecture"]), 850),
                margin={"l": 40, "b": 0, "t": 10, "r": 40},
                legend=dict(orientation="h", x=0, y=-0.4),
                yaxis={"title": "R2 score"},
            ),
        }
    elif value_organ == "All":
        distinct_architectures = df_res.architecture.drop_duplicates()
        plots = []
        df_res["organ"] = (
            df_res["organ"]
            .replace("*instances01", "I01")
            .replace("*instances23", "I23")
            .replace("*instances1.5x", "I1.5x")
        )

        for archi in distinct_architectures:
            df_res_archi = df_res[df_res.architecture == archi]
            df_res_archi["view"] = df_res_archi["view"] + " - " + df_res_archi["transformation"]
            df_res_archi["view"] = df_res_archi["view"].str.replace("- raw", "")
            hovertemplate = (
                "Model : %{x}\
                             <br>Algorithm : "
                + archi
                + "<br>Score : %{y}<br> Sample Size : %{customdata}"
            )

            plot_test = Bar(
                x=[df_res_archi["organ"].values, df_res_archi["view"].values],
                y=df_res_archi[metric],
                error_y=dict(type="data", array=df_res_archi[std]),
                hovertemplate=hovertemplate,
                customdata=df_res_archi["N_all"],
                name=archi,
            )
            plots.append(plot_test)

        d = {
            "data": plots,
            "layout": dict(
                height=600,
                width=3500,
                margin={"l": 20, "b": 250, "t": 10, "r": 0},
                bargap=0,
                xaxis=dict(tickfont=dict(size=8)),
                yaxis={"title": "R2 score"},
            ),
        }

    else:  # value_organ in ['Heart', 'Liver', 'Pancreas']:
        df_res = df_res[df_res.organ == value_organ]
        distinct_architectures = df_res.architecture.drop_duplicates()
        plots = []
        for archi in distinct_architectures:
            df_res_archi = df_res[df_res.architecture == archi]
            hovertemplate = (
                "Model : %{x}\
                             <br>Architecture : "
                + archi
                + "<br>Score : %{y}<br> Sample Size : %{customdata}"
            )
            plot_test = Bar(
                x=[df_res_archi["view"].values, df_res_archi["transformation"].values],
                y=df_res_archi[metric],
                error_y=dict(type="data", array=df_res_archi[std]),
                hovertemplate=hovertemplate,
                customdata=df_res_archi["N_all"],
                name=archi,
            )
            plots.append(plot_test)
        d = {
            "data": plots,
            "layout": dict(
                height=600,
                width=max(25 * len(df_res["architecture"]), 850),
                margin={"l": 40, "b": 150, "t": 10, "r": 40},
                yaxis={"title": "R2 score"},
            ),
        }

    return Figure(d)
