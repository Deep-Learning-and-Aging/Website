import dash_html_components as html
from dash_website import COLORS_SECTIONS, BACKGROUND_COLORS_SECTIONS


def get_text_color():
    text = html.Div(
        [
            html.P(
                "The Datasets pages present the different datasets which we leverage to predict chronological age, classified by data modalities: Scalar data, time series, images and videos."
            ),
            html.Br(),
            html.Div(
                html.H4("Scalars"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The Scalars page can be used to explore the distribution of the different scalar biomarkers which we leveraged to predict chronological age. It includes three plots: (1) an histogram of the biomarker for males and females participants, (2) a scatter plot with regression line showing the association of the biomarker with age in a univariate, linear context, and (3) a volcano plot showing how the biomarkers in the same category are associated with chronological age."
            ),
            html.P(
                "A table summarizing the correlation, regression coefficient and associated p-value for male, females, and all participants can also be found."
            ),
            html.P(
                "To allow the different plots and statistics to be dynamically computed in a reasonable time, we are only using a subset of the full 676,787 samples (XX TODO which size Samuel?)."
            ),
            html.P(
                "Select the scalar biomarker of interest by selecting its biological “dimension” (e.g Brain), its biological “subdimension” (e.g Cognitive) and its biological “sub-subdimension” (e.g Reaction Time). Finally, select the biomarker (e.g mean time to correctly identify matches)."
            ),
            html.P(
                "It is possible to limit the analysis to a subset of the UKB cohort using the demographic filters (age, sex, ethnicity)."
            ),
            html.Br(),
            html.Div(
                html.H4("Time series"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The Time Series page can be used to visualize samples from the different time series datasets we leveraged to predict chronological age. Select the biological dimension (e.g Physical Activity), subdimension (e.g FullWeek) and sub-subdimension (e.g TimeSeriesFeatures), as well as the channel, that is the biomarker that is measured over time (e.g XXTODO). Then select the sex and age group of the sample you would like to visualize. Ten samples are available for each combination above, so select one of them in the sample list. It is possible to display two samples simultaneously for comparison purposes."
            ),
            html.Br(),
            html.Div(
                html.H4("Images"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The Images page is highly similar to the Time Series page and can be used to visualize samples from the different images datasets we leveraged to predict chronological age. Select the biological dimension (e.g Musculoskeletal), subdimension (e.g Spine) and sub-subdimension (e.g Sagittal). Then select the sex and age group of the sample you would like to visualize. Ten samples are available for each combination above, so select one of them in the sample list. It is possible to display two samples simultaneously for comparison purposes."
            ),
            html.Br(),
            html.Div(
                html.H4("Videos"),
                style={
                    "text-indent": 0,
                },
            ),
            html.P(
                "The Video page is highly similar to the Images page and can be used to visualize samples from the video datasets we leveraged to predict chronological age. Select the biological dimension (Heart), subdimension (MRI) and sub-subdimension (“3 chambers Raw Videos” or “3 chambers Raw Videos”). Then select the sex and age group of the sample you would like to visualize. Ten samples are available for each combination above, so select one of them in the sample list. Click on the image to launch the gif. You will probably want to zoom as the images are only 200*200 pixels. It is possible to display two samples simultaneously for comparison purposes."
            ),
        ],
        style={
            "background-color": BACKGROUND_COLORS_SECTIONS["datasets"],
            "fontSize": 18,
            "padding": 30,
            "text-align": "justify",
            "text-indent": 30,
        },
    )

    return text, COLORS_SECTIONS["datasets"]
