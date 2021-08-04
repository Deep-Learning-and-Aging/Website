import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "The phenotypic correlation page has two tabs. One for displaying the heatmap of the correlations between selected aging dimensions [33 principal aging dimensions], and one displaying the heatmap of the correlations between all the aging dimensions [All 331 aging dimensions]."
        ),
        html.P(
            "The page displays an interactive heatmap. Hovering over an element will display the correlation between accelerated aging in the two aging dimensions, along with the R-Squared values obtained when predicting chronological age for the two aging dimensions."
        ),
        html.Div(html.P("Samples can be defined in three ways:"), style={"text-indent": 0}),
        html.P(
            "- Participant and time of examination: If several samples were collected from the same participant, each is treated as sample for the models. This maximizes the sample size."
        ),
        html.P(
            "- Participant (average across samples) - We took the average across the different samples if more than one sample was collected from a participant at different ages. For example, brain MRI images were collected during UKB’s second and third instances, whereas blood biomarkers were collected during the zeroth and first instances. This approach reduces sample size but allows the comparison between aging dimensions for which the data were not collected simultaneously by UKB."
        ),
        html.P(
            "- Participant and time when possible, otherwise average - The definition of “Participant and time of examination” is applied when it is possible, to maximize sample size. When two datasets were not simultaneously collected and would result in an intersection of sample size 0, the second definition is used instead."
        ),
        html.Div(html.P("Aging dimensions can be ordered by:"), style={"text-indent": 0}),
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
