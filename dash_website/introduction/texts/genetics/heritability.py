import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "We performed a GWAS on each of the main accelerated aging dimensions, as well as some selected accelerated aging subdimensions. We report the genes and SNPs we identified (GWAS), the heritability of each phenotype (Heritability) and the genetic correlation between the aging dimensions (Correlation)."
        ),
        html.Br(),
        html.Div(
            html.H4("GWAS"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "The GWAS results can be visualized using two different plots: A Manhattan plot, and a Volcano plot. Each plot is displayed on its separate tab."
        ),
        html.Br(),
        html.Div(
            html.H6("Manhattan Plot"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "A Manhattan plot displaying the results of the GWAS for each accelerated aging dimension is available. “All” can also be selected in the list of dimensions to display a union of all the GWASs. For each chromosome, the SNP with the lowest p-value is annotated with the name of the gene it belongs to."
        ),
        html.P(
            "We display the associated Quantile-Quantile plot to allow for the estimation of p-value inflation, as well."
        ),
        html.Br(),
        html.Div(
            html.H6("Volcano Plot"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "The volcano plot presents the same results as the Manhattan plot, but it only includes the significant findings. The plot is interactive and hovering over a data point will display the SNP number, the name of the gene, the gene type. If “All” is selected as the dimension, it will also display the accelerated aging dimension from which the association comes."
        ),
        html.Br(),
        html.Div(
            html.H4("Heritability"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "This bar plot summarizes, for each accelerated aging dimension, which percentage of its variance could be explained by genetic factors (heritability)."
        ),
        html.Br(),
        html.Div(
            html.H4("Correlation"),
            style={
                "text-indent": 0,
            },
        ),
        html.P(
            "We computed the genetic correlation (r_g) between accelerated aging dimensions when the sample size allowed it. The results are displayed on an interactive heatmap. Hovering over an element displays the genetic correlation, as well as the name of the two aging dimensions involved, their associated R-Squared value when used to predict chronological age, and their associated genetic heritability, for context. Similarly to the Phenotypic Correlation plot, the rows and columns of the heatmap can be ordered by (1) genetic heritability (Score), (2) based on the a priori biological similarities between aging dimensions (Custom), or (3) based on the hierarchical clustering performed on these dimensions using the genetic correlation as a distance metric. In the latter case, the hierarchical clustering is displaying above the attention map."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
