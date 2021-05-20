import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "Comparison between the correlations from the four previous pages. For example, are the aging dimensions that are strongly phenotypically correlated the same as the aging dimensions that are strongly genetically correlated?"
        ),
        html.P(
            "In the scatter plot, the x-coordinate of a data point is: the correlation between (first_X-category, aging_dimension_a) and (first_X-category, aging dimension_b). The y-coordinate of a data point is: the correlation between (second_category, aging_dimension_a) and (second_category, aging dimension_b)."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
