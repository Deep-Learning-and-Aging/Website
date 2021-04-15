import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_csv
from dash_website import DIMENSIONS, ALL_CATEGORIES

DICT_TO_CHANGE_DIMENSIONS = {
    "ImmuneSystem": "BloodCells",
    "\*": "set",
    "*instances01": "set_instances01",
    "*instances1.5x": "set_instances1.5x",
    "*instances23": "set_instances23",
}
DICT_TO_FORMER_DIMENSIONS = {value: key for key, value in DICT_TO_CHANGE_DIMENSIONS.items()}
DICT_TO_CHANGE_CATEGORIES = {
    "HeartSize": "HeartFunction",
    "AnthropometryImpedance": "Impedance",
    "AnthropometryBodySize": "Anthropometry",
    "Claudification": "Claudication",
}
DICT_TO_FORMER_CATEGORIES = {value: key for key, value in DICT_TO_CHANGE_CATEGORIES.items()}

DICT_TO_FORMER_ALGORITHM = {
    "elastic_net": "ElasticNet",
    "light_gbm": "LightGbm",
    "neural_network": "NeuralNetwork",
    "correlation": "Correlation",
}


if __name__ == "__main__":
    list_features = []
    for category in tqdm(pd.Index(ALL_CATEGORIES).drop(["Genetics", "Phenotypic", "PhysicalActivity"])):
        for dimension in DIMENSIONS:
            for algorithm in ["elastic_net", "light_gbm", "neural_network", "correlation"]:
                if "medical_diagnoses_" in category:
                    features = load_csv(
                        f"page18_MultivariateXWASFeatures/FeatureImp_{DICT_TO_FORMER_CATEGORIES.get(category, category)}_{DICT_TO_FORMER_DIMENSIONS.get(dimension, dimension)}_{DICT_TO_FORMER_ALGORITHM.get(algorithm, algorithm)}.csv"
                    ).rename(columns={"features": "variable", "weight": "feature_importance"})
                else:
                    features = load_csv(
                        f"page18_MultivariateXWASFeatures/FeatureImp_Clusters_{DICT_TO_FORMER_CATEGORIES.get(category, category)}_{DICT_TO_FORMER_DIMENSIONS.get(dimension, dimension)}_{DICT_TO_FORMER_ALGORITHM.get(algorithm, algorithm)}.csv"
                    ).rename(columns={"features": "variable", "weight": "feature_importance"})

                features["variable"] = features["variable"].apply(lambda variable: variable.split(".0")[0])
                features["category"] = category
                features["dimension"] = dimension
                features["algorithm"] = algorithm

                list_features.append(features)

    pd.concat(list_features).reset_index(drop=True).to_feather(
        "data/xwas/multivariate_feature_importances/feature_importances.feather"
    )
