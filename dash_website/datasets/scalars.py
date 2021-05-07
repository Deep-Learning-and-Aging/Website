from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash

import pandas as pd
import numpy as np
from scipy.stats import linregress
from sklearn.linear_model import LinearRegression

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_drop_down, get_range_slider, get_options
from dash_website import DOWNLOAD_CONFIG
from dash_website.datasets import TREE_SCALARS, ETHNICITIES, SEX_VALUE, SEX_COLOR


def get_layout():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_scalars"), dcc.Store(id="linear_regression_scalars")]),
            html.H1("Datasets - Scalars"),
            html.Br(),
            html.Br(),
            dbc.Row(dbc.Col(dbc.Card(get_controls_scalars())), justify="center"),
            dbc.Row(dbc.Col(dbc.Card(get_subcontrols_scalars())), justify="center"),
            dbc.Row(html.Br()),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_distribution_scalars"),
                        dcc.Graph(id="figure_distribution_scalars", config=DOWNLOAD_CONFIG),
                    ]
                ),
                justify="center",
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_values_scalars"),
                        html.H6(id="subtitle_values_scalars"),
                        dcc.Graph(id="figure_values_scalars", config=DOWNLOAD_CONFIG),
                    ]
                ),
                justify="center",
            ),
            dbc.Row(
                dcc.Loading(
                    [
                        html.H4(id="title_volcano_scalars"),
                        dcc.Graph(id="figure_volcano_scalars", config=DOWNLOAD_CONFIG),
                    ]
                ),
                justify="center",
            ),
        ],
        fluid=True,
    )


@APP.callback(
    Output("memory_scalars", "data"),
    [
        Input("dimension_scalars", "value"),
        Input("subdimension_scalars", "value"),
        Input("sub_subdimension_scalars", "value"),
    ],
)
def _modify_store_scalars(dimension, subdimension, sub_subdimension):
    return load_feather(f"datasets/scalars/{dimension}_{subdimension}_{sub_subdimension}.feather").to_dict()


@APP.callback(
    Output("linear_regression_scalars", "data"),
    [Input("memory_scalars", "data"), Input("age_range_scalars", "value")],
)
def _modify_store_linear_regression(data_scalars, age_range):
    scalars = pd.DataFrame(data_scalars).set_index(["sex", "id"])
    scalars.drop(
        index=scalars[
            (scalars["chronological_age"] > age_range[1]) | (scalars["chronological_age"] < age_range[0])
        ].index,
        inplace=True,
    )

    list_indexes = []

    for sex in ["all", "male", "female"]:
        for observation in ["slope", "intercept", "p_value", "correlation", "sample_size"]:
            list_indexes.append([sex, observation])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["sex", "observation"])
    linear_regression = pd.DataFrame(
        None, index=indexes, columns=scalars.columns.drop(["chronological_age"] + ETHNICITIES)
    )

    for feature in scalars.columns.drop(["chronological_age"] + ETHNICITIES):
        linear_regressor = LinearRegression()
        linear_regressor.fit(scalars.reset_index(level="sex")[["sex"] + ETHNICITIES], scalars["chronological_age"])
        corrected_chronological_age = scalars["chronological_age"] - linear_regressor.predict(
            scalars.reset_index(level="sex")[["sex"] + ETHNICITIES]
        )

        linear_regressor = LinearRegression()
        linear_regressor.fit(scalars.reset_index(level="sex")[["sex"] + ETHNICITIES], scalars[feature])
        corrected_feature = scalars[feature] - linear_regressor.predict(
            scalars.reset_index(level="sex")[["sex"] + ETHNICITIES]
        )

        linear_regression.loc[("all", "correlation"), feature] = corrected_feature.corr(
            corrected_chronological_age, method="pearson"
        )

        for sex in ["male", "female"]:
            linear_regressor_sex = LinearRegression()
            linear_regressor_sex.fit(
                scalars.loc[SEX_VALUE[sex], ETHNICITIES], scalars.loc[SEX_VALUE[sex], "chronological_age"]
            )
            corrected_chronological_age_sex = scalars.loc[
                SEX_VALUE[sex], "chronological_age"
            ] - linear_regressor_sex.predict(scalars.loc[SEX_VALUE[sex], ETHNICITIES])

            linear_regressor_sex = LinearRegression()
            linear_regressor_sex.fit(scalars.loc[SEX_VALUE[sex], ETHNICITIES], scalars.loc[SEX_VALUE[sex], feature])
            corrected_feature_sex = scalars.loc[SEX_VALUE[sex], feature] - linear_regressor_sex.predict(
                scalars.loc[SEX_VALUE[sex], ETHNICITIES]
            )

            linear_regression.loc[(sex, "correlation"), feature] = corrected_feature_sex.corr(
                corrected_chronological_age_sex, method="pearson"
            )

        slope, intercept, _, p_value, _ = linregress(scalars["chronological_age"], scalars[feature])

        linear_regression.loc[("all", "slope"), feature] = slope
        linear_regression.loc[("all", "intercept"), feature] = intercept
        linear_regression.loc[("all", "p_value"), feature] = p_value
        linear_regression.loc[("all", "sample_size"), feature] = scalars.shape[0]

        for sex in ["male", "female"]:
            slope_sex, intercept_sex, _, p_value_sex, _ = linregress(
                scalars.loc[SEX_VALUE[sex], "chronological_age"], scalars.loc[SEX_VALUE[sex], feature]
            )

            linear_regression.loc[(sex, "slope"), feature] = slope_sex
            linear_regression.loc[(sex, "intercept"), feature] = intercept_sex
            linear_regression.loc[(sex, "p_value"), feature] = p_value_sex
            linear_regression.loc[(sex, "sample_size"), feature] = scalars.loc[SEX_VALUE[sex]].shape[0]

    return linear_regression.reset_index().to_dict()


def get_controls_scalars():
    first_dimension = list(TREE_SCALARS.keys())[0]
    first_subdimension = list(TREE_SCALARS[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_scalars", list(TREE_SCALARS.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_scalars",
            list(TREE_SCALARS[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_item_radio_items(
            "sub_subdimension_scalars",
            TREE_SCALARS[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
        get_range_slider("age_range_scalars", 35, 85, "Filter with an age range : "),
    ]


@APP.callback(
    [
        Output("subdimension_scalars", "options"),
        Output("subdimension_scalars", "value"),
        Output("sub_subdimension_scalars", "options"),
        Output("sub_subdimension_scalars", "value"),
    ],
    [Input("dimension_scalars", "value"), Input("subdimension_scalars", "value")],
)
def _change_subdimensions(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_scalars":
        first_subdimension = list(TREE_SCALARS[dimension].keys())[0]
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            list(TREE_SCALARS[dimension].keys())[0],
            get_options(TREE_SCALARS[dimension][first_subdimension]),
            TREE_SCALARS[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            subdimension,
            get_options(TREE_SCALARS[dimension][subdimension]),
            TREE_SCALARS[dimension][subdimension][0],
        )


def get_subcontrols_scalars():
    return (get_drop_down("feature_scalars", [""], "Select feature :", from_dict=False),)


@APP.callback(
    [Output("feature_scalars", "options"), Output("feature_scalars", "value")], Input("memory_scalars", "data")
)
def _change_feature(scalars_data):
    features = pd.DataFrame(scalars_data).columns.drop(["id", "sex", "chronological_age"] + ETHNICITIES)

    return get_options(features), features[0]


@APP.callback(
    [Output("figure_distribution_scalars", "figure"), Output("title_distribution_scalars", "children")],
    [
        Input("feature_scalars", "value"),
        Input("age_range_scalars", "value"),
        Input("memory_scalars", "data"),
    ],
)
def _change_distribution(feature, age_range, data_scalars):
    import plotly.graph_objs as go

    scalars = pd.DataFrame(data_scalars).set_index(["sex", "id"])
    scalars.drop(
        index=scalars[
            (scalars["chronological_age"] > age_range[1]) | (scalars["chronological_age"] < age_range[0])
        ].index,
        inplace=True,
    )

    fig = go.Figure()

    for sex in ["male", "female"]:
        fig.add_histogram(
            x=scalars.loc[SEX_VALUE[sex], feature],
            name=sex.capitalize(),
            histnorm="percent",
            marker={"color": SEX_COLOR[sex]},
        )

    fig.update_layout(
        width=2000, height=500, xaxis_title_text="Value", yaxis_title_text="Count (in %)", bargap=0.2, bargroupgap=0.1
    )

    return fig, "Histogram of " + feature


@APP.callback(
    [
        Output("figure_values_scalars", "figure"),
        Output("title_values_scalars", "children"),
        Output("subtitle_values_scalars", "children"),
    ],
    [
        Input("feature_scalars", "value"),
        Input("age_range_scalars", "value"),
        Input("linear_regression_scalars", "data"),
        Input("memory_scalars", "data"),
    ],
)
def _change_scatter(feature, age_range, data_linear_regresion, data_scalars):
    import plotly.graph_objs as go

    scalars = pd.DataFrame(data_scalars).set_index(["sex", "id"])
    scalars = pd.DataFrame(data_scalars).set_index(["sex", "id"])
    scalars.drop(
        index=scalars[
            (scalars["chronological_age"] > age_range[1]) | (scalars["chronological_age"] < age_range[0])
        ].index,
        inplace=True,
    )

    linear_regression = pd.DataFrame(data_linear_regresion).set_index(["sex", "observation"])

    fig = go.Figure()

    fig.add_scattergl(
        y=scalars[feature],
        x=scalars["chronological_age"],
        name=feature,
        opacity=0.8,
        marker={"color": "Grey", "size": 2},
        mode="markers",
    )

    fig.add_scatter(
        y=linear_regression.loc[("all", "slope"), feature] * np.array([age_range[0], age_range[1]])
        + linear_regression.loc[("all", "intercept"), feature],
        x=[age_range[0], age_range[1]],
        name="All",
        line={"color": "Black"},
        marker={"size": 0.1},
    )

    for sex in ["male", "female"]:
        fig.add_scatter(
            y=linear_regression.loc[(sex, "slope"), feature] * np.array([age_range[0], age_range[1]])
            + linear_regression.loc[(sex, "intercept"), feature],
            x=[age_range[0], age_range[1]],
            name=sex.capitalize(),
            line={"color": SEX_COLOR[sex]},
            marker={"size": 0.1},
        )

    fig.update_layout(width=2000, height=500, xaxis_title_text="Chronological Age")

    return (
        fig,
        f"Scatter plot of {feature}",
        f"p-value : {linear_regression.loc[('all', 'p_value'), feature].round(3)}, correlation : {linear_regression.loc[('all', 'correlation'), feature].round(3)} and regression coefficient : {linear_regression.loc[('all', 'slope'), feature].round(3)}",
    )


@APP.callback(
    [Output("figure_volcano_scalars", "figure"), Output("title_volcano_scalars", "children")],
    [Input("linear_regression_scalars", "data"), Input("feature_scalars", "value")],
)
def _change_volcano(data_linear_regresion, feature):
    import plotly.graph_objs as go

    linear_regression = pd.DataFrame(data_linear_regresion).set_index(["sex", "observation"])

    fig = go.Figure()

    hovertemplate = "Feature : %{customdata[0]}\
                        <br>p-value : %{customdata[1]:.3f}\
                        <br>Correlation : %{x:.3f}\
                        <br>Sample Size : %{customdata[2]}\
                        <br>Regression coefficient : %{customdata[3]:.3f}"
    customdata = np.stack(
        [
            linear_regression.columns,
            linear_regression.loc[("all", "p_value")],
            linear_regression.loc[("all", "sample_size")],
            linear_regression.loc[("all", "slope")],
        ],
        axis=-1,
    )

    fig.add_scatter(
        x=linear_regression.loc[("all", "correlation")],
        y=-np.log10((linear_regression.loc[("all", "p_value")] + 1e-323).to_list()),
        mode="markers",
        name="all",
        hovertemplate=hovertemplate,
        customdata=customdata,
        marker={"color": "Black"},
    )

    for sex in ["male", "female"]:
        hovertemplate_sex = "Feature : %{customdata[0]}\
                            <br>p-value : %{customdata[1]:.3f}\
                            <br>Correlation : %{x:.3f}\
                            <br>Sample Size : %{customdata[2]}\
                            <br>Regression coefficient : %{customdata[3]:.3f}"
        customdata_sex = np.stack(
            [
                linear_regression.columns,
                linear_regression.loc[(sex, "p_value")],
                linear_regression.loc[(sex, "sample_size")],
                linear_regression.loc[(sex, "slope")],
            ],
            axis=-1,
        )

        fig.add_scatter(
            x=linear_regression.loc[(sex, "correlation")],
            y=-np.log10((linear_regression.loc[(sex, "p_value")] + 1e-323).to_list()),
            mode="markers",
            name=sex.capitalize(),
            hovertemplate=hovertemplate_sex,
            customdata=customdata_sex,
            marker={"color": SEX_COLOR[sex]},
        )

    fig.add_scatter(
        x=[
            linear_regression.loc[("all", "correlation")].min() - linear_regression.loc[("all", "correlation")].std(),
            linear_regression.loc[("all", "correlation")].max() + linear_regression.loc[("all", "correlation")].std(),
        ],
        y=[-np.log10(0.05), -np.log10(0.05)],
        name="No correction",
        mode="lines",
        marker={"size": 0.1},
    )
    fig.add_scatter(
        x=[
            linear_regression.loc[("all", "correlation")].min() - linear_regression.loc[("all", "correlation")].std(),
            linear_regression.loc[("all", "correlation")].max() + linear_regression.loc[("all", "correlation")].std(),
        ],
        y=[
            -np.log(0.05 / linear_regression.loc[("all", "sample_size")][0]),
            -np.log(0.05 / linear_regression.loc[("all", "sample_size")][0]),
        ],
        name="With Bonferoni correction for all",
        mode="lines",
        marker={"size": 0.1},
    )

    fig.update_layout(width=2000, height=500, yaxis_title_text="-log(p_value)", xaxis_title_text="Pearson correlation")

    return fig, "Volcano plot for all features"
