import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We treated the time series as 1D images and used saliency attention maps to identify the most influential time steps."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
