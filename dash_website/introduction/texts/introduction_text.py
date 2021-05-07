import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            [
                "This website presents the results of our publication “Analyzing the multidimensionality of biological aging with the tools of deep learning across diverse image-based and physiological indicators yields robust age predictors” which can be found ",
                html.A("here", href="https://www.medrxiv.org/content/10.1101/2021.04.25.21255767v1"),
                ".",
            ]
        ),
        html.P(
            "We analyzed 676,787 samples from 502,211 UK Biobank participants aged 37-82 years with the tools of deep learning to build a total of 331 chronological age predictors on different data modalities such as videos (e.g heart magnetic resonance imaging [MRI] videos), images (e.g brain, liver and pancreas MRIs, full body X-rays, eye fundus and optical coherence tomography [OCT] images, carotid ultrasound images), time-series (e.g electrocardiograms [ECGs], pulse wave analysis, wrist accelerometer data) and scalar data (e.g blood biomarkers, anthropometric measures) to characterize the multiple dimensions of aging. We combined these age predictors into 28 ensemble models based on specific organ systems. We then defined accelerated agers as participants whose predicted age was greater than their chronological age and computed the phenotypic correlation between these 28 definitions of accelerated aging. We estimated the shared genetic and environmental architecture, or correlation, between different aging dimensions and we performed genome wide association studies [GWASs] on the 28 accelerated aging dimensions to estimate the heritability of these phenotypes and identify single nucleotide polymorphisms [SNPs]. Then we performed a data driven search to identify biomarkers, phenotypes and environmental variables associated with the different dimensions of accelerated aging. Overall, we show that most dimensions of aging are complex traits with both genetic and non-genetic correlates. These dimensions are weakly correlated with each other, highlighting the multidimensionality of the aging process."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
