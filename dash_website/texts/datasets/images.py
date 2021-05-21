import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "The Images page can be used to visualize samples from the different images datasets we leveraged to predict chronological age."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
