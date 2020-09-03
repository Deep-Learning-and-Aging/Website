import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


from app import app

layout = html.Div([
    dbc.Card([
        dbc.Jumbotron(
            [
                html.H1("Multi-Dimensionality of Aging"),
                html.P(
                    "Introduction ",
                    className="lead",
                ),
                html.Hr(className="my-1"),
                html.P(
                    """
                    This dash app presents the results of our paper "Name Paper". We used the UK Biobank resource with different types of data (Images, Time Series, Tabular) to try to predict Age. The biomarkers are blood biomarkers (e.g cholesterol, glucose, albumin), urine biomarkers (e.g urine albumin) and anthropometrics (e.g height, BMI, blood pressure)

                    The results are organized in eight parts: "Biomarkers", "Correlations", "Predictabilities" and "Regression coefficients". For each of those indicators, we calculated baseline values (using data from the full age range) and examined the trajectories with age. For both baseline values and age trajectories, we compared the results between sexes and ethnicities (Non-Hispanic Whites, Hispanics and Non-Hispanic Blacks).

                    For the details about each of those indicators, please see the tabs on the navigation bar, and advice on how to best use the features of the app in the respective window below.
                    """
                ),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Biomarkers : ", className = 'lead'),
                html.P("In this page we study the different tabular data features. For each feature, we can see its distribution, how it is linearly related to the Age, and if the feature is significant in Aging"),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Age prediction performances : ", className = 'lead'),
                html.P("We can see how the different models (Images, TimeSeries, Tabular) perform predicting Age. Different metrics are available R2 score and RMSE"),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Features importances : ", className = 'lead'),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Attention Maps : ", className = 'lead'),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Linear XWAS : ", className = 'lead'),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Multivariate XWAS : ", className = 'lead'),
                html.Br(),
                html.Hr(className="my-1"),
                html.P("Correlation between accelerated aging dimensions : ", className = 'lead')
        ]
        )
    ]),
], id = 'id_menu')
