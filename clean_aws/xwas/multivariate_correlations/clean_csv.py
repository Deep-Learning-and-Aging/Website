import pandas as pd
from dash_website.utils.aws_loader import load_csv

DICT_TO_CHANGE_DIMENSIONS = {
    "ImmuneSystem": "BloodCells",
    "\*": "set",
    "*instances01": "set_instances01",
    "*instances1.5x": "set_instances1.5x",
    "*instances23": "set_instances23",
}
DICT_TO_CHANGE_CATEGORIES = {
    "HeartSize": "HeartFunction",
    "AnthropometryImpedance": "Impedance",
    "AnthropometryBodySize": "Anthropometry",
    "Claudification": "Claudication",
}

CAMEL_TO_SNAKE = {"ElasticNet": "elastic_net", "LightGbm": "light_gbm", "NeuralNetwork": "neural_network"}

if __name__ == "__main__":
    list_correlations = []

    for correlation_type in ["Pearson", "Spearman"]:
        for algorithm in ["ElasticNet", "LightGbm", "NeuralNetwork"]:
            correlations = load_csv(
                f"page8_MultivariateXWASCorrelations/CorrelationsMultivariate/CorrelationsMultivariate_{correlation_type}_{algorithm}.csv",
                index_col=0,
            )

            correlations.rename(
                columns={
                    "env_dataset": "category",
                    "organ_1": "dimension_1",
                    "organ_2": "dimension_2",
                    "corr": "correlation",
                    "sample_size": "number_variables",
                },
                inplace=True,
            )
            correlations.replace(DICT_TO_CHANGE_DIMENSIONS, inplace=True)

            correlations["category"] = list(
                map(
                    lambda list_category: list_category[1] if len(list_category) > 1 else list_category[0],
                    correlations["category"].str.split("_"),
                )
            )

            correlations.replace(DICT_TO_CHANGE_CATEGORIES, inplace=True)

            correlations["algorithm"] = CAMEL_TO_SNAKE[algorithm]
            correlations["correlation_type"] = correlation_type.lower()

            list_correlations.append(correlations)
    every_correlation = pd.concat(list_correlations).set_index(["algorithm", "correlation_type"])

    list_columns = []
    for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
        for correlation_type in ["pearson", "spearman", "number_variables"]:
            list_columns.append([algorithm, correlation_type])
    columns = pd.MultiIndex.from_tuples(list_columns)
    correlations_raw = pd.DataFrame(
        None,
        index=every_correlation.set_index(["dimension_1", "dimension_2", "category"]).index.drop_duplicates(),
        columns=columns,
    )

    for algorithm in ["elastic_net", "light_gbm", "neural_network"]:
        for correlation_type in ["pearson", "spearman"]:
            correlations_raw[(algorithm, correlation_type)] = (
                every_correlation.loc[(algorithm, correlation_type)]
                .reset_index(drop=True)
                .set_index(["dimension_1", "dimension_2", "category"])["correlation"]
            )

            correlations_raw[(algorithm, "number_variables")] = (
                every_correlation.loc[(algorithm, correlation_type)]
                .reset_index(drop=True)
                .set_index(["dimension_1", "dimension_2", "category"])["number_variables"]
            )

    correlations_raw.columns = map(str, correlations_raw.columns.tolist())
    correlations_raw.reset_index().to_feather("data/xwas/multivariate_correlations/correlations/correlations.feather")
