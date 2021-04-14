import dash_html_components as html
from dash_website import COLORS_SECTIONS, BACKGROUND_COLORS_SECTIONS


def get_text_color():
    text = html.Div(
        [
            html.P("We performed an X-Wide Analysis Study for each accelerated aging dimension."),
            html.Br(),
            html.Div(
                html.H4("Univariate XWAS - Associations"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "First, we computed the partial correlation between accelerated aging and each biomarker, phenotype or environmental variable. We display the results using interactive volcano plots. The table of partial correlations can also be found below the volcano plot."
            ),
            html.P("One must select the aging dimension for which the XWAS will be displayed."),
            html.P(
                "An option can be selected to display either all associations, or only the association of a specific category, such as biomarkers."
            ),
            html.P(
                "The associations displayed can be further refined by selecting a list of specific X datasets, such as Alcohol or Diet, for example. Alternatively, the volcano plot is interactive: clicking on a specific X-category (e.g Alcohol) in the legend will disable it, and clicking again will re-display it. Quickly double-clicking will only display the category."
            ),
            html.Br(),
            html.Div(
                html.H4("Univariate XWAS - Correlations"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "For each pair of accelerated aging dimensions and for each X-dataset, we computed the correlation between the associations reported under Univariate XWAS - Associations. Intuitively, we for example estimated whether drinking alcohol had a similar effect on brain aging and heart aging, or not. One way to think about the results is as a 3D matrix: two dimensions for a normal correlation matrix, and a third dimension for the different layers (i.e the different X datasets). The results are therefore displayed as “slices” of this 3D array, using interactive attention maps. We use two different tabs to present the results. The first tab “X-dataset” displays the correlation between all aging dimensions, one X-dataset at the time. In contrast, the second tab “Aging dimension” displays the correlation between a specific aging dimension (one at a time) and all the other ones for all the X-datasets."
            ),
            html.Br(),
            html.Div(
                html.H6("Correlations by X-dataset"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The heatmap displays the correlation between the XWAS associations for all pairs of accelerated aging dimensions. A specific X-dataset such as Alcohol or Sleep must be selected. The correlations displayed can either be the Pearson (default) or the Spearman correlation. For these correlations, we can either consider the X-variables that were significantly associated with either accelerated aging dimensions (Union, the default), with both accelerated aging dimensions (Intersection), or to simply consider all X-variables independently of the significance or their association (All). The heatmap is interactive and displays correlation value, along with the two aging dimensions involved and the sample size of the correlation."
            ),
            html.Br(),
            html.Div(
                html.H6("Correlations by aging dimension"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "As mentioned under “Univariate XWAS - Correlations”, this heatmap is highly similar to the one described under “Correlations by X-dataset”, with the difference that instead of selecting a specific X-dataset to display its matching “slice” in the 3D array, one must select a specific aging dimension, to obtain a slice in a perpendicular direction."
            ),
            html.Br(),
            html.Div(
                html.H4("Multivariate XWAS - Prediction of accelerated aging"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "We build multivariate models to predict accelerated aging in each aging dimension using elastic nets, light GBMs and neural networks. The resulting testing R-Squared values are displayed in an interactive heatmap. Hovering over an element will display the accelerated aging dimension, the X-dataset, the R-Squared value and the sample size of the dataset on which the model was built."
            ),
            html.P(
                "Options allow to select a specific subset of X-datasets, such as biomarkers only, for example. By default, the R-Squared values displayed correspond to the best performing algorithm, but it is also possible to display the ones from either the elastic net, the GBM or the neural network."
            ),
            html.Br(),
            html.Div(
                html.H4("Multivariate XWAS - Feature importances"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "We display the feature importances of the models trained to predict accelerated aging in the different dimensions. The key parameters to select are the accelerated aging dimension and the X-dataset of interest. This page is otherwise highly similar to the one described under “Features importances - Scalars”."
            ),
            html.Br(),
            html.Div(
                html.H4("Multivariate XWAS - Correlations"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "This page displays the correlation between the feature importances displayed in the precedent page for each pair of accelerated aging dimensions. The parameters to select are (1) the algorithm used to predict accelerated aging, (2) the X-dataset that was used as predictors, and (3) the correlation type (Pearson or Spearman). Similarly to Univariate XWAS - Correlations, the results are available in two different tabs. One tab showing the correlation heatmap between all aging dimensions, one X-dataset at the time (Correlations by X-dataset) and one tab with a heatmap showing the correlation between one specific aging dimension with all the other and for all X datasets (Correlations by aging dimension)."
            ),
        ],
        style={
            "background-color": BACKGROUND_COLORS_SECTIONS["xwas"],
            "fontSize": 18,
            "padding": 30,
            "text-align": "justify",
            "text-indent": 30,
        },
    )

    return text, COLORS_SECTIONS["xwas"]
