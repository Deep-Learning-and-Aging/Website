import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES


if __name__ == "__main__":
    list_indexes = []
    for dimension in DIMENSIONS + ["All_aging_dimensions"]:
        for category in MAIN_CATEGORIES_TO_CATEGORIES["All"] + [
            f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()
        ]:
            list_indexes.append([dimension, category])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["dimension", "category"])

    list_columns = []
    for item in ["total", "significant", "accelerated_aging", "decelerated_aging"]:
        if item == "total":
            observations = ["total"]
        else:
            observations = ["number", "percentage"]
        for observation in observations:
            list_columns.append([item, observation])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["item", "observation"])

    summary = pd.DataFrame(None, index=indexes, columns=columns)

    for dimension in tqdm(DIMENSIONS):
        correlations_dimension = load_feather(
            f"xwas/univariate_results/linear_correlations_{dimension}.feather",
            columns=["category", "p_value", "correlation"],
        )

        for group in correlations_dimension.groupby(by=["category"]):
            category = group[0]
            summary.loc[(dimension, category), ("total", "total")] = group[1].shape[0]
            summary.loc[(dimension, category), ("significant", "number")] = (
                group[1]["p_value"] < 0.05 / group[1].shape[0]
            ).sum()
            summary.loc[(dimension, category), ("accelerated_aging", "number")] = (
                (group[1]["p_value"] < 0.05 / group[1].shape[0]) & (group[1]["correlation"] < 0)
            ).sum()
            summary.loc[(dimension, category), ("decelerated_aging", "number")] = (
                (group[1]["p_value"] < 0.05 / group[1].shape[0]) & (group[1]["correlation"] > 0)
            ).sum()

        for main_category, categories in MAIN_CATEGORIES_TO_CATEGORIES.items():
            group = correlations_dimension.set_index("category").loc[categories]

            summary.loc[(dimension, f"All_{main_category}"), ("total", "total")] = group.shape[0]
            summary.loc[(dimension, f"All_{main_category}"), ("significant", "number")] = (
                group["p_value"] < 0.05 / group.shape[0]
            ).sum()
            summary.loc[(dimension, f"All_{main_category}"), ("accelerated_aging", "number")] = (
                (group["p_value"] < 0.05 / group.shape[0]) & (group["correlation"] < 0)
            ).sum()
            summary.loc[(dimension, f"All_{main_category}"), ("decelerated_aging", "number")] = (
                (group["p_value"] < 0.05 / group.shape[0]) & (group["correlation"] > 0)
            ).sum()

        for item in ["significant", "accelerated_aging", "decelerated_aging"]:
            summary.loc[dimension, (item, "percentage")] = (
                summary.loc[dimension, (item, "number")] / summary.loc[dimension, ("total", "total")]
            ).values

    column_without_percentage = [
        ("total", "total"),
        ("significant", "number"),
        ("accelerated_aging", "number"),
        ("decelerated_aging", "number"),
    ]

    for category in MAIN_CATEGORIES_TO_CATEGORIES["All"] + [
        f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()
    ]:
        summary.loc[("All_aging_dimensions", category), column_without_percentage] = (
            summary.swaplevel().loc[category, column_without_percentage].sum()
        )

    for item in ["significant", "accelerated_aging", "decelerated_aging"]:
        summary.loc["All_aging_dimensions", (item, "percentage")] = (
            summary.loc["All_aging_dimensions", (item, "number")]
            / summary.loc["All_aging_dimensions", ("total", "total")]
        ).values

    summary.columns = map(str, summary.columns.tolist())
    summary.reset_index().to_feather("data/xwas/univariate_results/summary.feather")