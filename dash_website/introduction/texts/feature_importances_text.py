import dash_html_components as html
from dash_website import COLORS_SECTIONS, BACKGROUND_COLORS_SECTIONS


def get_text_color():
    text = html.Div(
        [
            html.P(
                "For interpretability purposes, we share the feature importance for our models. The methods used to identify the features driving the prediction differ between models built on scalar data, time series, images and videos."
            ),
            html.Br(),
            html.Div(
                html.H4("Scalars"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "For the models built on scalar data, we assess the feature importance differently based on the algorithm. For the elastic net, we report the absolute value of the regression coefficient (normalized). For the light GBM, we report the feature importance which is computed as a function of the number of splits involving the variable. For neural networks, we randomly shuffled each predictor across the samples and computed the associated decrease in R-Squared. We also defined a “feature importance” in terms of the absolute value of the univariate correlation between each scalar biomarker and chronological age. This allows to identify which features are initially associated with age, and whether they remain good age predictors when incorporated in a model."
            ),
            html.P(
                "We display the predictors’ feature importance as a bar plot, by decreasing order of feature importance for the best predicting algorithm, which can be read above the bar bar plot (usually the light GBM). By hovering over the interactive plot, it is possible to read the numerical value associated with each bar."
            ),
            html.P(
                "For now, the only target available is Age. Select the dimension, subdimension and sub-subdimension of your interest (e.g Brain - Cognitive - Reaction Time) and the matching bar plot will be displayed, along with the table with the raw numbers below."
            ),
            html.P(
                "We also report the correlation between feature importance as defined by the three algorithms (elastic net, light GBM, neural network), as well as defined by univariate correlations with chronological age. These correlations are displayed in a 4x4 table, and are available for both Pearson and Spearman correlation."
            ),
            html.Br(),
            html.Div(
                html.H4("Time series"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "For the models built on time series, we treated the time series as 1D images and used saliency attention maps to identify the most influential time steps. Select the aging main dimension (e.g Physical Activity), subdimension (e.g FullWeek) and sub-subdimension (e.g Acceleration) as well as the channel to display (e.g “1”). At the top of the page, the architecture of the model that best predicted chronological age on this dataset will be displayed, along with the associated R-Squared and sample size, for context. You can then select the sex (male or female), age group (younger end of the age distribution, middle of the distribution, or older end of the distribution) and aging rate (accelerated ager, normal ager, decelerated ager) of your interest. Finally, you can select one of the ten representative samples available for this category. The attention map will then be displayed, along with the chronological age and predicted biological age of this participant."
            ),
            html.P("It is possible to select two samples simultaneously, for comparison purposes."),
            html.Br(),
            html.Div(
                html.H4("Images"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "For the models built on images, we used two kinds of attention maps: saliency maps and Grad-RAM (Gradient-weighted Regression Activation Mapping) to identify which regions and features were driving the prediction for each image. Aside from that, the page is very similar to the one for Time Series. Select the aging main dimension (e.g Musculoskeletal), subdimension (e.g Spine) and sub-subdimension (e.g Sagittal). At the top of the page, the architecture of the model that best predicted chronological age on this dataset will be displayed, along with the associated R-Squared and sample size, for context. You can then select the sex (male or female), age group (younger end of the age distribution, middle of the distribution, or older end of the distribution) and aging rate (accelerated ager, normal ager, decelerated ager) of your interest. Finally, you can select one of the ten representative samples available for this category. The attention map will then be displayed, along with the chronological age and predicted biological age of this participant. By default, both the raw image, the saliency map and the Grad-RAM maps are displayed. Untick the matching boxes to visualize different filters combinations."
            ),
            html.P("It is possible to select two samples simultaneously, for comparison purposes."),
            html.Br(),
            html.Div(
                html.H4("Videos"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "For the models built on videos, we used saliency maps to identify which regions and features were driving the prediction for each time frame. Aside from that, the page is very similar to the one for Images. Select the aging main dimension (Heart), subdimension (MRI) and sub-subdimension (e.g 4 chambers raw). At the top of the page, the architecture of the model that best predicted chronological age on this dataset will be displayed, along with the associated R-Squared and sample size, for context. You can then select the sex (male or female), age group (younger end of the age distribution, middle of the distribution, or older end of the distribution) and aging rate (accelerated ager, normal ager, decelerated ager) of your interest. Finally, you can select one of the ten representative samples available for this category. The attention map will then be displayed, along with the chronological age and predicted biological age of this participant. When the video is halted, the gif shows the summary attention maps across all time frames. Click on the image to launch the gif."
            ),
        ],
        style={
            "background-color": BACKGROUND_COLORS_SECTIONS["feature_importances"],
            "fontSize": 18,
            "padding": 30,
            "text-align": "justify",
            "text-indent": 30,
        },
    )

    return text, COLORS_SECTIONS["feature_importances"]
