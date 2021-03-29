import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_csv

from dash_website import DIMENSIONS, ALL_CATEGORIES

if __name__ == "__main__":

    list_columns = []

    for dimension in tqdm(DIMENSIONS):
        for category in ALL_CATEGORIES:
            for variable in load_csv(
                f"page5_LinearXWASResults/LinearOutput/linear_correlations_{category}_{dimension}.csv",
                usecols=["env_feature_name"],
            )["env_feature_name"]:
                list_columns.append([dimension, category, variable])

    columns = pd.MultiIndex.from_tuples(list_columns, names=["dimension", "category", "variable"])
    correlations = pd.DataFrame(None, index=["p_value", "correlation", "sample_size"], columns=columns)

    for dimension in tqdm(DIMENSIONS):
        for category in tqdm(ALL_CATEGORIES):
            correlation_category_dimension = load_csv(
                f"page5_LinearXWASResults/LinearOutput/linear_correlations_{category}_{dimension}.csv",
                usecols=["env_feature_name", "p_val", "corr_value", "size_na_dropped"],
            ).set_index("env_feature_name")
            correlation_category_dimension.index.name = "varaible"
            correlation_category_dimension.columns = ["p_value", "correlation", "sample_size"]
            correlations[(dimension, category)] = correlation_category_dimension.T

    correlations.columns = map(str, correlations.columns.tolist())
    correlations.reset_index().to_feather("linear_correlations.feather")
