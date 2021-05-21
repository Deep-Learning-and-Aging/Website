import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We performed an X-Wide Association Study for 33 selected aging dimensions. These correlations are reported under “XWAS - Univariate Associations”."
        ),
        html.P(
            "For each X-category and pair of aging dimension, we measured whether accelerated aging is similarly associated with the X-variables in two aging dimensions. Intuitively, we, for example, estimated whether drinking alcohol had a similar effect on brain aging and heart aging, or not. One way to think about the results is as a 3D matrix: two dimensions for a normal correlation matrix between aging dimensions, and a third dimension for the different layers (the different X-categories). The results are therefore displayed as “slices” of this 3D array, using interactive attention maps. "
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
        html.Div(
            html.P(
                "When computing the correlation between aging dimensions in terms of association with X-variables, we only took into account X-variables that are statistically significantly associated with accelerated aging. We did it in three different ways:"
            ),
            style={
                "text-indent": 0,
            },
        ),
        html.P("- Union: the union of the significant variables from the two aging dimensions are taken into account."),
        html.P("- All: all the variables from the two aging dimensions are taken into account."),
        html.P(
            "- Intersection: the intersection between the significant variables from the two aging dimensions are taken into account."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
