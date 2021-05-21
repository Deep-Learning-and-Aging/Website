import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We assess the feature importance differently based on the algorithm. For the elastic net, we report the absolute value of the regression coefficient (normalized). For the light GBM, we report the feature importance which is computed as a function of the number of splits involving the variable. For neural networks, we used a permutation test (we randomly shuffled each predictor across the samples and computed the associated decrease in R-Squared). We also defined a “feature importance” as the absolute value of the univariate correlation between each scalar variable and chronological age. This allows us to identify which features are initially linearly associated with chronological age, and whether they remain good age predictors when incorporated in a multivariate model."
        ),
        html.P(
            "We display the predictors’ feature importance as a bar plot, by decreasing order of feature importance for the best predicting algorithm, which can be read above the bar plot."
        ),
        html.P(
            "We also report the correlation between feature importance as defined by the three algorithms (elastic net, light GBM, neural network), as well as defined by univariate correlations with chronological age. These correlations are displayed in the 4x4 table."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
