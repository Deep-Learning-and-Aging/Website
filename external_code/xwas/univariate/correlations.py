import pandas as pd
import numpy as np
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS

SQUEEZED_DIMENSIONS = load_feather("xwas/squeezed_dimensions_participant_and_time_of_examination.feather").set_index(
    "squeezed_dimensions"
)


def load_correlation(key_in_aws):
    correlation_dimension = load_feather(key_in_aws)
    correlation_dimension.drop(
        index=correlation_dimension.index[correlation_dimension["sample_size"] < 10], inplace=True
    )

    return correlation_dimension.set_index(["category", "variable"])


if __name__ == "__main__":
    list_indexes = []
    for squeezed_dimension_1 in DIMENSIONS:
        for squeezed_dimension_2 in DIMENSIONS:
            for category in MAIN_CATEGORIES_TO_CATEGORIES["All"] + [
                f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()
            ]:
                list_indexes.append([squeezed_dimension_1, squeezed_dimension_2, category])
    indexes = pd.MultiIndex.from_tuples(
        list_indexes, names=["squeezed_dimension_1", "squeezed_dimension_2", "category"]
    )

    list_columns = []
    for method in ["all", "union", "intersection"]:
        for correlation_type in ["pearson", "spearman", "number_variables"]:
            list_columns.append([method, correlation_type])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["method", "correlation_type"])
    correlations = pd.DataFrame(None, index=indexes, columns=columns)
    correlations.reset_index(inplace=True)

    for index_dimension in ["1", "2"]:
        correlations = correlations.set_index(f"squeezed_dimension_{index_dimension}")
        correlations[f"dimension_{index_dimension}"] = SQUEEZED_DIMENSIONS["dimension"]
        correlations[f"subdimension_{index_dimension}"] = SQUEEZED_DIMENSIONS["subdimension"]
        correlations.reset_index(inplace=True)
    correlations.set_index(["squeezed_dimension_1", "squeezed_dimension_2", "category"], inplace=True)

    phenotypic = load_feather("xwas/univariate_correlations/phenotypic.feather").set_index(
        ["squeezed_dimension_1", "squeezed_dimension_2"]
    )
    genetics = load_feather("xwas/univariate_correlations/genetics.feather").set_index(
        ["squeezed_dimension_1", "squeezed_dimension_2"]
    )

    for squeezed_dimension_1 in tqdm(DIMENSIONS):
        correlation_dimension_1 = load_correlation(
            f"xwas/univariate_results/linear_correlations_{RENAME_DIMENSIONS.get(squeezed_dimension_1, squeezed_dimension_1)}.feather"
        )
        for squeezed_dimension_2 in DIMENSIONS:
            correlation_dimension_2 = load_correlation(
                f"xwas/univariate_results/linear_correlations_{RENAME_DIMENSIONS.get(squeezed_dimension_2, squeezed_dimension_2)}.feather"
            )

            for category in MAIN_CATEGORIES_TO_CATEGORIES["All"] + [
                f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()
            ]:
                if category in ["Phenotypic", "Genetics"]:
                    continue
                if "All" in category:
                    categories = MAIN_CATEGORIES_TO_CATEGORIES[category.split("_")[1]].copy()
                    if category.split("_")[1] == "All":
                        categories.remove("Phenotypic")
                        categories.remove("Genetics")
                else:
                    categories = [category]

                correlations_1 = correlation_dimension_1.loc[categories]
                correlations_2 = correlation_dimension_2.loc[categories]

                indexes = {}

                indexes["all"] = correlations_1.index.intersection(correlations_2.index)

                indexes["union"] = correlations_1.index[
                    correlations_1["p_value"] < 0.05 / correlations_1.shape[0]
                ].union(correlations_2.index[correlations_2["p_value"] < 0.05 / correlations_2.shape[0]])
                if (~indexes["union"].isin(correlations_1.index)).sum() > 0:
                    correlations_to_add = pd.DataFrame(
                        None,
                        index=indexes["union"][~indexes["union"].isin(correlations_1.index)],
                        columns=["p_value", "correlation", "sample_size"],
                    )
                    correlations_to_add["correlation"] = 0

                    correlations_1 = correlations_1.append(correlations_to_add)
                if (~indexes["union"].isin(correlations_2.index)).sum() > 0:
                    correlations_to_add = pd.DataFrame(
                        None,
                        index=indexes["union"][~indexes["union"].isin(correlations_2.index)],
                        columns=["p_value", "correlation", "sample_size"],
                    )
                    correlations_to_add["correlation"] = 0

                    correlations_2 = correlations_2.append(correlations_to_add)

                indexes["intersection"] = correlations_1.index[
                    correlations_1["p_value"] < 0.05 / correlations_1.shape[0]
                ].intersection(correlations_2.index[correlations_2["p_value"] < 0.05 / correlations_2.shape[0]])

                for method in ["all", "union", "intersection"]:
                    for correlation_type in ["pearson", "spearman"]:
                        if len(indexes[method]) <= 1:
                            correlations.loc[
                                (squeezed_dimension_1, squeezed_dimension_2, category), (method, correlation_type)
                            ] = np.nan
                        else:
                            correlations.loc[
                                (squeezed_dimension_1, squeezed_dimension_2, category), (method, correlation_type)
                            ] = correlations_1.loc[indexes[method], "correlation"].corr(
                                correlations_2.loc[indexes[method], "correlation"], method=correlation_type
                            )
                        correlations.loc[
                            (squeezed_dimension_1, squeezed_dimension_2, category), (method, "number_variables")
                        ] = len(indexes[method])

            if squeezed_dimension_1 == "EyesAll" or squeezed_dimension_2 == "EyesAll":
                continue
            for method in ["all", "union", "intersection"]:
                for correlation_type in ["pearson", "spearman"]:
                    correlations.loc[
                        (squeezed_dimension_1, squeezed_dimension_2, "Phenotypic"), (method, correlation_type)
                    ] = phenotypic.loc[(squeezed_dimension_1, squeezed_dimension_2), "correlation"]
                    correlations.loc[
                        (squeezed_dimension_1, squeezed_dimension_2, "Genetics"), (method, correlation_type)
                    ] = genetics.loc[(squeezed_dimension_1, squeezed_dimension_2), "correlation"]

    correlations = (
        correlations.reset_index()
        .drop(columns=["squeezed_dimension_1", "squeezed_dimension_2"])
        .set_index(["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "category"])
    )
    correlations.columns = map(str, correlations.columns.tolist())
    correlations.reset_index().to_feather("all_data/xwas/univariate_correlations/correlations.feather")
