import dash_html_components as html


TEXT = html.Div(
    [
        html.P("We performed an X-Wide Analysis Study for each accelerated aging dimension."),
        html.P(
            "We computed the partial correlation between accelerated aging and each X-variable [Volcano]. We report the number and proportion of X-variables significantly associated with accelerated/decelerated aging [Summary]."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
