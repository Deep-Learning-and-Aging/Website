import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We built multivariate models to predict the accelerated aging in each aging dimension from the variables of each X-category. We used elastic nets, light GBMs and neural networks. The resulting testing R-Squared values are displayed in “XWAS - Accelerated aging prediction performance”. This page displays the correlation between the feature importances for each pair of accelerated aging dimensions. One way to think about the results is as a 3D matrix: two dimensions for a normal correlation matrix, and a third dimension for the different layers (the different X-categories). The results are therefore displayed as “slices” of this 3D array, using interactive attention maps."
        ),
        html.Div(
            html.P("We use three different tabs to present the results:"),
            style={
                "text-indent": 0,
            },
        ),
        html.P("- By category: displays the correlation between all aging dimensions, one X-category at the time."),
        html.P(
            "- By aging dimension: displays the correlation between a specific aging dimension (one at a time) and all the other aging dimensions for all the X-categories."
        ),
        html.P(
            "- Summary: For each X-category, displays the average correlation between a selected aging dimension and all the other aging dimensions in terms of association with the X-variables. If two specific aging dimensions are selected instead of “average”, the correlations match the correlations displayed under the  “by Aging dimension” tab."
        ),
        html.Div(
            html.P("For the tab “By category”, aging dimensions can be ordered by:"),
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
