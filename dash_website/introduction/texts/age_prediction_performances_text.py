import dash_html_components as html
from dash_website import COLORS_SECTIONS, BACKGROUND_COLORS_SECTIONS


def get_text_color():
    text = html.Div(
        [
            html.P(
                "This page presents the prediction performances for the different models we used to predict age using a bar plot."
            ),
            html.P(
                "The first option, “Samples” vs. “Individuals” allows to see the prediction performance when one prediction is generated for each participant’s sample, versus the prediction when, for each participant, the predictions for the different samples collected from the same participant are averaged to estimate his/her age (see the publication for more detail). By default, “Samples” is selected."
            ),
            html.P(
                "The second option allows to only display a subset of the models for clarity purposes. “Main dimensions” displays the results for the 33 ensemble models built for each main aging dimension and selected aging sub-dimension, whereas “All models” displays the results for all 331 models built on avery single main dimension, subdimension, sub-subdimension using different algorithms. Ensemble models are different levels are also included and marked with a “*” to show the level at which the ensemble was performed (more details available in the publication). Finally, non-ensemble models are also available to display."
            ),
            html.P(
                "We provide an option to select an aging main dimension to only display the models that belong to this dimension. This feature is most helpful when selecting “All models” in the option above, and for example allows you to focus on all the Heart related age predictions."
            ),
            html.P(
                "Finally, different metrics can be selected to evaluate the performances of the different models. By default, R-Squared values are displayed."
            ),
            html.P(
                "The bar plot is interactive, hovering over a bar will display its numeric value (e.g R-squared or RMSE), along with the sample size of the dataset on which the model was built."
            ),
        ],
        style={
            "background-color": BACKGROUND_COLORS_SECTIONS["age_prediction_performances"],
            "fontSize": 18,
            "padding": 30,
            "text-align": "justify",
            "text-indent": 30,
        },
    )

    return text, COLORS_SECTIONS["age_prediction_performances"]
