import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "The Video page can be used to visualize samples from the video datasets we leveraged to predict chronological age. Click on the image to launch the gif."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
