import dash_html_components as html
from dash_website import COLORS_SECTIONS, BACKGROUND_COLORS_SECTIONS


def get_text_color():
    text = html.Div(
        [
            html.P(
                "The phenotypic correlation page has two tabs. For displaying the heatmap of the correlations between the different aging dimensions, and one displaying the result of a hierarchical clustering on these dimensions using the correlation as the distance metric."
            ),
            html.Br(),
            html.Div(
                html.H6("Heatmap"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The page displays an interactive heatmap. Hovering over an element will display the R-Squared value obtained when predicting chronological age for the two dimensions involved in the correlation, as well as the value of the correlation itself."
            ),
            html.P(
                "The first option is to select whether to display the correlation based on accelerated aging computed for each sample, or based on the average accelerated aging rate for each participant (taking the average across the different samples if more than one sample was collected from a participant at different ages). By default, the second option is selected, as it allows us to compare accelerated aging from data modalities that were not simultaneously collected. For example, brain MRI images we collected during UKB’s second and third instances, whereas blood biomarkers were collected during the zeroth and first instances. Therefore, the sample size of the intersection between these two datasets is zero, which prevents us from reporting the correlation between accelerated aging in these two dimensions when “instances” is selected. In contrast, by looking at accelerated aging participant-wise (“eid”), we can estimate whether participants who were accelerated agers in terms of biochemistry during the first instances were also the ones who were accelerated agers in terms of brain MRI images during later instances."
            ),
            html.P(
                "We provide a third option: “*”, which displays the instances-based correlation when available, and the participants-based correlation otherwise."
            ),
            html.P(
                "The second option is to decide whether to display only the main aging dimensions and selected subdimensions, or all the dimensions. If “All models” is selected, then it also becomes possible to select a main dimension of which to focus, so as to only display the correlation between brain aging subdimensions, for example."
            ),
            html.P(
                "Finally, the rows and columns of the correlation heatmap can be ordered in three different ways. (1) By R-Squared values of their corresponding aging dimension when predicting chronological age (Score), (2) based on a priori similarities between the aging dimensions, such as having heart and arterial dimensions next to each other (Custom TODO rename), and (3) based on the similarities between aging dimensions in terms of accelerated aging correlation (Clustering). When clustering is chosen, the hierarchical clustering which yielded the order is displayed at the top of the heatmap."
            ),
            html.Br(),
            html.Div(
                html.H6("Clustering"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The Clustering tab mirrors the Heatmap tab, but instead of displaying the correlation heatmap, it solely displays the hierarchical clustering obtained by performing the eponyme algorithm on the correlation heatmap."
            ),
        ],
        style={
            "background-color": BACKGROUND_COLORS_SECTIONS["correlation"],
            "fontSize": 18,
            "padding": 30,
            "text-align": "justify",
            "text-indent": 30,
        },
    )

    return text, COLORS_SECTIONS["correlation"]
