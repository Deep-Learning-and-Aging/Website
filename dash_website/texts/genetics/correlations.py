import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We performed a Genome Wide Association Study (GWAS) on 33 selected aging dimensions. We report the genetic correlation between the aging dimensions."
        ),
        html.P(
            "We computed the genetic correlation between accelerated aging dimensions when the sample size allowed it. The results are displayed on an interactive heatmap. Hovering over an element displays the genetic correlation, as well as the name of the two aging dimensions involved, their associated R-Squared value when used to predict chronological age (R²), and their associated GWAS-based heritability (h²), for context."
        ),
        html.Div(
            html.P("Aging dimensions can be ordered by:"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "- Custom order - The aging dimensions are ordered by a predefined order, highlighting the biological similarities between aging dimensions."
        ),
        html.P(
            "- Clustering - The order is based on the similarities between aging dimensions     in terms of accelerated aging correlation. The hierarchical clustering is displayed above the attention map."
        ),
        html.P(
            "- R² - The order is determined by the R-Squared values of the aging dimension when predicting chronological age."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
