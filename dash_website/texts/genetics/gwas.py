import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "The Genome Wide Association Study (GWAS) results can be visualized using two different plots: A Manhattan plot [Manhattan & QQ plots], and a Volcano plot [Volcano plot]."
        ),
        html.P(
            "The Manhattan plot displays the results of the GWAS for each accelerated aging dimension. “All” can also be selected in the list of dimensions to display a union of all the GWASs. For each chromosome, the SNP with the lowest p-value is annotated with the name of the gene it belongs to."
        ),
        html.P(
            "We display the associated Quantile-Quantile plot to allow for the estimation of p-value inflation, as well."
        ),
        html.P(
            "The volcano plot presents the same results as the Manhattan plot, but it only includes the significant findings."
        ),
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
