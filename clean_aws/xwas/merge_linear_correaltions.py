import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_csv

from dash_website import DIMENSIONS, ALL_CATEGORIES

if __name__ == "__main__":

    for dimension in tqdm(DIMENSIONS):
        list_indexes = []
        for category in ALL_CATEGORIES:
            for variable in load_csv(
                f"page5_LinearXWASResults/LinearOutput/linear_correlations_{category}_{dimension}.csv",
                usecols=["env_feature_name"],
            )["env_feature_name"].apply(lambda variable: variable.replace(".0", "")):
                list_indexes.append([category, variable])

        indexes = pd.MultiIndex.from_tuples(list_indexes, names=["category", "variable"])
        correlations = pd.DataFrame(None, columns=["p_value", "correlation", "sample_size"], index=indexes)

        for category in ALL_CATEGORIES:
            correlation_category_dimension = load_csv(
                f"page5_LinearXWASResults/LinearOutput/linear_correlations_{category}_{dimension}.csv",
                usecols=["env_feature_name", "p_val", "corr_value", "size_na_dropped"],
            )
            correlation_category_dimension["env_feature_name"] = correlation_category_dimension[
                "env_feature_name"
            ].apply(lambda variable: variable.replace(".0", ""))
            correlation_category_dimension.set_index("env_feature_name", inplace=True)
            correlation_category_dimension.index.name = "variable"
            correlation_category_dimension.columns = ["p_value", "correlation", "sample_size"]

            correlations.loc[category] = correlation_category_dimension.values

        correlations.index = map(str, correlations.index.tolist())
        correlations.reset_index().to_feather(f"data/xwas/univariate_results/linear_correlations_{dimension}.feather")
