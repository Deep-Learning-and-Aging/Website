import pandas as pd

STUDIED_DIMENSION = "Eye"
RENAMING = {
    "Eyes": "General",
    "EyesFundus": "Fundus",
    "EyesOCT": "OCT",
    "EyesAll": "All",
    "ClinicalPhenotypes": "Clinical Phenotypes",
    "FamilyHistory": "Family History",
    "Environmental": "Environmental variables",
    "Socioeconomics": "Socioeconomic variables",
}

STUDIED_SUBDIMENSIONS = list(
    pd.Index(RENAMING.keys()).drop(["ClinicalPhenotypes", "FamilyHistory", "Environmental", "Socioeconomics"])
)
RENAMING_COLUMNS = {
    "dimension": f"{STUDIED_DIMENSION} Dimension",
    "category": "X - main category",
    "subcategory": "X - subcategory",
    "variable": "Variable",
    "correlation": "Partial correlation",
    "p_value": "p-value",
    "sample_size": "Sample size",
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
    [dimension, main_category] for dimension in STUDIED_SUBDIMENSIONS for main_category in ORDER_MAIN_CATEGORIES
]


if __name__ == "__main__":
    from dash_website import MAIN_CATEGORIES_TO_CATEGORIES

    correlations_list = []
    for studied_subdimension in STUDIED_SUBDIMENSIONS:
        clean_dimension = (
            pd.read_csv(f"external_code/publication_figures/univariate_correlations/raw/{studied_subdimension}.csv")
            .drop(columns="Unnamed: 0")
            .rename(columns={"category": "subcategory"})
        )
        clean_dimension["dimension"] = studied_subdimension
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
    ).to_csv(
        f"external_code/publication_figures/univariate_correlations/{STUDIED_DIMENSION}_XWAS_univariate_correlations.csv"
    )
