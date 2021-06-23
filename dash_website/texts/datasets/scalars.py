import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "Here, you can explore the distribution of the different scalar variables which we leveraged to predict chronological age. "
        ),
        html.Div(html.P("It includes three plots:"), style={"text-indent": 0}),
        html.P("- a histogram of the variables for male and female participants."),
        html.P(
            "- a scatter plot with a regression line showing the association of the variable with age in a univariate, linear context."
        ),
        html.P(
            "- a volcano plot showing how the variables in the same category are associated with chronological age."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
