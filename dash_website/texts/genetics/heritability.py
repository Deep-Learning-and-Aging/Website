import dash_html_components as html


TEXT = html.Div(
    [
        html.P(
            "This bar plot summarizes, for each accelerated aging dimension, which percentage of its variance could be explained by the SNPs (GWAS-based heritability)."
        )
    ],
    style={
        "fontSize": 18,
        "padding": 30,
        "text-align": "justify",
        "text-indent": 30,
    },
)
