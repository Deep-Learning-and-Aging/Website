import pandas as pd

RENAMING_COLUMNS = {
    "dimension": "Heart Dimension",
    "category": "X - main category",
    "subcategory": "X - subcategory",
    "variable": "Variable",
    "correlation": "Partial correlation",
    "p_value": "p-value",
    "sample_size": "Sample size",
}
RENAMING = {
    "Heart": "General",
    "HeartECG": "Electrical (ECG-based)",
    "HeartMRI": "Anatomical (MRI-based)",
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
    for dimension in ["Heart", "HeartECG", "HeartMRI"]
    for main_category in ORDER_MAIN_CATEGORIES
]


if __name__ == "__main__":
    correlations = (
        pd.read_csv("Heart_univariate_correlations.csv")
        .drop(columns="Unnamed: 0")
        .rename(columns={"category": "subcategory"})
    )

    from dash_website import MAIN_CATEGORIES_TO_CATEGORIES

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
    ).to_csv("Heart.csv")
