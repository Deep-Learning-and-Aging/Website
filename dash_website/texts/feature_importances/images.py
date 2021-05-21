import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We used two kinds of attention maps: saliency maps and Grad-RAM (Gradient-weighted Regression Activation Mapping) to identify which regions and features were driving the prediction for each image."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
