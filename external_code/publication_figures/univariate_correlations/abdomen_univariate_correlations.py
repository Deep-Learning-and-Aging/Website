import pandas as pd

RENAMING_COLUMNS = {
    "dimension": "Abdomen Dimension",
    "category": "X - main category",
    "subcategory": "X - subcategory",
    "variable": "Variable",
    "correlation": "Partial correlation",
    "p_value": "p-value",
    "sample_size": "Sample size",
}
RENAMING = {
    "Abdomen": "General",
    "AbdomenLiver": "Liver",
    "AbdomenPancreas": "Pancreas",
    "ClinicalPhenotypes": "Clinical Phenotypes",
    "FamilyHistory": "Family History",
    "Environmental": "Environmental variables",
    "Socioeconomics": "Socioeconomic variables",
}
ORDER_MAIN_CATEGORIES = [
    "Biomarkers",
    "ClinicalPhenotypes",
    "Diseases",
    "FamilyHistory",
    "Environmental",
    "Socioeconomics",
]
ORDER_DIMENSIONS_MAIN_CATEGORIES = [
    [dimension, main_category]
    for dimension in ["Abdomen", "AbdomenLiver", "AbdomenPancreas"]
    for main_category in ORDER_MAIN_CATEGORIES
]


if __name__ == "__main__":
    from dash_website import MAIN_CATEGORIES_TO_CATEGORIES

    correlations_list = []
    for abdomen_dimension in ["Abdomen", "AbdomenLiver", "AbdomenPancreas"]:
        clean_dimension = (
            pd.read_csv(f"external_code/publication_figures/univariate_correlations/{abdomen_dimension}.csv")
            .drop(columns="Unnamed: 0")
            .rename(columns={"category": "subcategory"})
        )
        clean_dimension["dimension"] = abdomen_dimension
        correlations_list.append(clean_dimension)

    correlations = pd.concat(correlations_list, ignore_index=True)

    correlations.set_index("subcategory", inplace=True)
    correlations["category"] = None

    for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys():
        if main_category == "All":
            continue
        correlations.loc[
            correlations.index.isin(MAIN_CATEGORIES_TO_CATEGORIES[main_category]), "category"
        ] = main_category

    correlations.loc["FamilyHistory", "category"] = "FamilyHistory"
    correlations.reset_index(inplace=True)

    correlations_sorted = (
        correlations.sort_values(by=["dimension", "category", "subcategory", "p_value"])
        .set_index(["dimension", "category"])
        .loc[ORDER_DIMENSIONS_MAIN_CATEGORIES]
        .reset_index()
    )

    correlations_sorted.replace(RENAMING)[RENAMING_COLUMNS].rename(columns=RENAMING_COLUMNS).reset_index(
        drop=True
    ).to_csv("external_code/publication_figures/univariate_correlations/Abdomen_XWAS_univariate_correlations.csv")
