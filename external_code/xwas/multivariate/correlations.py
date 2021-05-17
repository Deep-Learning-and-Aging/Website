import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather, upload_file
from dash_website import DIMENSIONS

VARIABLES_TO_DROP = [
    "Ethnicity.White",
    "Ethnicity.British",
    "Ethnicity.Irish",
    "Ethnicity.White_Other",
    "Ethnicity.Mixed",
    "Ethnicity.White_and_Black_Caribbean",
    "Ethnicity.White_and_Black_African",
    "Ethnicity.White_and_Asian",
    "Ethnicity.Mixed_Other",
    "Ethnicity.Asian",
    "Ethnicity.Indian",
    "Ethnicity.Pakistani",
    "Ethnicity.Bangladeshi",
    "Ethnicity.Asian_Other",
    "Ethnicity.Black",
    "Ethnicity.Caribbean",
    "Ethnicity.African",
    "Ethnicity.Black_Other",
    "Ethnicity.Chinese",
    "Ethnicity.Other",
    "Ethnicity.Other_ethnicity",
    "Ethnicity.Do_not_know",
    "Ethnicity.Prefer_not_to_answer",
    "Ethnicity.NA",
    "Sex",
    "Age when attended assessment centre",
]
SQUEEZED_DIMENSIONS = load_feather("xwas/squeezed_dimensions_participant_and_time_of_examination.feather")[
    ["dimension", "subdimension", "squeezed_dimensions"]
].set_index("squeezed_dimensions")


if __name__ == "__main__":
    features = load_feather("xwas/multivariate_feature_importances/feature_importances.feather")

    list_index = []
    for squeezed_dimension_1 in DIMENSIONS:
        for squeezed_dimension_2 in DIMENSIONS:
            for category in features["category"].drop_duplicates():
                list_index.append([squeezed_dimension_1, squeezed_dimension_2, category])
    indexes = pd.MultiIndex.from_tuples(list_index, names=["squeezed_dimension_1", "squeezed_dimension_2", "category"])

    list_columns = []
    for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
        for correlation_type in ["pearson", "spearman", "number_features"]:
            list_columns.append([algorithm, correlation_type])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["algorithm", "correlation_type"])

    correlations = pd.DataFrame(None, index=indexes, columns=columns)

    indexed_features = features.set_index(["dimension", "category", "algorithm", "variable"])
    for squeezed_dimension_1, squeezed_dimension_2, category in tqdm(correlations.index):
        for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
            for correlation_type in ["pearson", "spearman"]:
                correlations.loc[
                    (squeezed_dimension_1, squeezed_dimension_2, category), (algorithm, correlation_type)
                ] = (
                    indexed_features.loc[(squeezed_dimension_1, category, algorithm), "feature_importance"]
                    .drop(VARIABLES_TO_DROP)
                    .corr(
                        indexed_features.loc[(squeezed_dimension_2, category, algorithm), "feature_importance"].drop(
                            VARIABLES_TO_DROP
                        ),
                        method=correlation_type,
                    )
                )
            correlations.loc[(squeezed_dimension_1, squeezed_dimension_2, category), (algorithm, "number_features")] = (
                indexed_features.loc[(squeezed_dimension_1, category, algorithm), "feature_importance"]
                .drop(VARIABLES_TO_DROP)
                .shape[0]
            )

    correlations.reset_index(inplace=True)

    for index_dimension in [1, 2]:
        correlations.set_index(f"squeezed_dimension_{index_dimension}", inplace=True)
        correlations[f"dimension_{index_dimension}"] = SQUEEZED_DIMENSIONS["dimension"]
        correlations[f"subdimension_{index_dimension}"] = SQUEEZED_DIMENSIONS["subdimension"]
        correlations.reset_index(drop=True)

    correlations.set_index(["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "category"], inplace=True)
    correlations.columns = map(str, correlations.columns.tolist())

    correlations.reset_index().to_feather("all_data/xwas/multivariate_correlations/correlations/correlations.feather")
    upload_file(
        "all_data/xwas/multivariate_correlations/correlations/correlations.feather",
        "xwas/multivariate_correlations/correlations/correlations.feather",
    )
