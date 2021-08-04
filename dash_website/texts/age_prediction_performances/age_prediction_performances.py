import dash_html_components as html


TEXT = html.Div(
    [
        html.P("This page presents the prediction performances for the different models we used to predict age."),
        html.Div(html.P("Samples can be defined in two ways:"), style={"text-indent": 0}),
        html.P(
            "- Participant and time of examination: If several samples were collected from the same participant, each is treated as sample for the models. This maximizes the sample size."
        ),
        html.P(
            "- Participant (average across samples) - We took the average across the different samples if more than one sample was collected from a participant at different ages. For example, brain MRI images were collected during UKB’s second and third instances, whereas blood biomarkers were collected during the zeroth and first instances. This approach reduces sample size but allows the comparison between aging dimensions for which the data were not collected simultaneously by UKB."
        ),
        html.Div(html.P("The models displayed can be filtered using three options:"), style={"text-indent": 0}),
        html.P("- Custom dimensions: selected dimensions that are all ensemble models."),
        html.P("- All dimensions: all dimensions are displayed."),
        html.P("- Without ensemble models: all the models that are not ensemble models."),
        html.Div(html.P("Among the metrics that can be chosen, there are:"), style={"text-indent": 0}),
        html.P(
            "- C-index: the C-index when the prediction of the chronological age (i.e. the biological age) was taken as the risk of dying."
        ),
        html.P(
            "- C-index difference: the C-index with the biological age as the risk of dying minus the C-index with the chronological age as the risk of dying."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
