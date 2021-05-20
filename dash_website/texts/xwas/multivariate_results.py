import dash_html_components as html


TEXT = html.Div(
    [
        html.P("We performed an X-Wide Analysis Study for each accelerated aging dimension."),
        html.P(
            "We built multivariate models to predict accelerated aging in each aging dimension from the variables of each X-category. We used elastic nets, light GBMs and neural networks. The resulting testing R-Squared values are displayed in an interactive heatmap [View Heatmap]. Hovering over an element displays the accelerated aging dimension, the X-category, the R-Squared value and the sample size of the dataset on which the model was built."
        ),
        html.P(
            "The R-Squared values can be chosen to correspond to a specific algorithm or they can correspond to the best performing algorithm."
        ),
        html.P("The R-Squared can also be displayed as bar plots [View bar plot]."),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
