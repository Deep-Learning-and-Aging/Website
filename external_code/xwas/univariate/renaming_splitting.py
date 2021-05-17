from dash_website.utils.aws_loader import load_feather
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES

DICT_TO_CHANGE_DIMENSIONS = {"ImmuneSystem": "BloodCells"}
DICT_TO_CHANGE_CATEGORIES = {
    "HeartSize": "HeartFunction",
    "AnthropometryImpedance": "Impedance",
    "AnthropometryBodySize": "Anthropometry",
    # Main categories
    "All_Phenotypes": "All_ClinicalPhenotypes",
}


if __name__ == "__main__":
    linear_correlations = load_feather("xwas/univariate_results/linear_correlations.feather")

    linear_correlations_cleaned_dimensions = linear_correlations.set_index(["dimension", "category"]).rename(
        index=DICT_TO_CHANGE_DIMENSIONS, level="dimension"
    )
    linear_correlations_cleaned = linear_correlations_cleaned_dimensions.rename(
        index=DICT_TO_CHANGE_CATEGORIES, level="category"
    )
    linear_correlations_cleaned.reset_index().to_feather("data/xwas/univariate_results/linear_correlations.feather")

    for dimension in DIMENSIONS:
        if dimension in DICT_TO_CHANGE_DIMENSIONS.keys():
            dimension = DICT_TO_CHANGE_DIMENSIONS[dimension]
        linear_correlations_cleaned.loc[dimension].reset_index().to_feather(
            f"data/xwas/univariate_results/linear_correlations_{dimension}.feather"
        )

    summary = load_feather("xwas/univariate_results/summary.feather")

    summary_cleaned_dimensions = summary.set_index(["dimension", "category"]).rename(
        index=DICT_TO_CHANGE_DIMENSIONS, level="dimension"
    )
    summary_cleaned = summary_cleaned_dimensions.rename(index=DICT_TO_CHANGE_CATEGORIES, level="category")
    summary_cleaned.reset_index().to_feather("data/xwas/univariate_results/summary.feather")

    correlations = load_feather("xwas/univariate_correlations/correlations/correlations.feather")

    correlations_cleaned_dimensions_1 = correlations.set_index(["dimension_1", "dimension_2", "category"]).rename(
        index=DICT_TO_CHANGE_DIMENSIONS, level="dimension_1"
    )
    correlations_cleaned_dimensions = correlations_cleaned_dimensions_1.rename(
        index=DICT_TO_CHANGE_DIMENSIONS, level="dimension_2"
    )
    correlations_cleaned = correlations_cleaned_dimensions.rename(index=DICT_TO_CHANGE_CATEGORIES, level="category")
    correlations_cleaned.reset_index().to_feather("data/xwas/univariate_correlations/correlations/correlations.feather")

    for dimension in DIMENSIONS:
        if dimension in DICT_TO_CHANGE_DIMENSIONS.keys():
            dimension = DICT_TO_CHANGE_DIMENSIONS[dimension]
        correlations_cleaned.loc[dimension].reset_index().rename(columns={"dimension_2": "dimension"}).to_feather(
            f"data/xwas/univariate_correlations/correlations/dimensions/correlations_{dimension}.feather"
        )

    for category in MAIN_CATEGORIES_TO_CATEGORIES["All"] + [
        f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()
    ]:
        if category in DICT_TO_CHANGE_CATEGORIES.keys():
            category = DICT_TO_CHANGE_CATEGORIES[category]
        correlations_cleaned.swaplevel().swaplevel(i=0, j=1).loc[category].reset_index().to_feather(
            f"data/xwas/univariate_correlations/correlations/categories/correlations_{category}.feather"
        )

    averages_correlations = load_feather("xwas/univariate_correlations/averages_correlations.feather")

    averages_correlations_cleaned_dimensions = averages_correlations.set_index(["dimension", "category"]).rename(
        index=DICT_TO_CHANGE_DIMENSIONS, level="dimension"
    )
    averages_correlations_cleaned = averages_correlations_cleaned_dimensions.rename(
        index=DICT_TO_CHANGE_CATEGORIES, level="category"
    )
    averages_correlations_cleaned.reset_index().to_feather(
        "data/xwas/univariate_correlations/averages_correlations.feather"
    )
