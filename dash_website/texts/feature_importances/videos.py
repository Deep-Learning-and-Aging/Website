import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We used saliency maps to identify which regions and features were driving the prediction for each time frame. Click on the image to launch the gif."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
