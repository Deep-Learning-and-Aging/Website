import dash_html_components as html


TEXT = html.Div(
    [
        html.P("We performed an X-Wide Analysis Study for each accelerated aging dimension."),
        html.P(
            "We build multivariate models to predict accelerated aging in each aging dimension from the variables of each X-category. We used elastic nets, light GBMs and neural networks. The resulting testing R-Squared values are displayed in “XWAS - Accelerated aging prediction performance”."
        ),
        html.P(
            "Here, we display the feature importances of the models. We assess the feature importance differently based on the algorithm. For the elastic net, we report the absolute value of the regression coefficient (normalized). For the light GBM, we report the feature importance which is computed as a function of the number of splits involving the variable. For neural networks, we used a permutation test (we randomly shuffled each predictor across the samples and computed the associated decrease in R-Squared). We also defined a “feature importance” in terms of the absolute value of the univariate correlation between each scalar variable and residual of the prediction of chronological age from the aging dimension. This allows us to identify which features are initially associated with accelerated aging, and whether they remain good accelerated aging predictors when incorporated in a multivariate model."
        ),
        html.P(
            "We display the predictors’ feature importance as a bar plot, by decreasing order of feature importance for the best predicting algorithm, which can be read above the bar plot."
        ),
        html.P(
            "We also report the correlation between feature importance as defined by the three algorithms (elastic net, light GBM, neural network), as well as defined by univariate correlations with the residual. These correlations are displayed in the 4x4 table."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
