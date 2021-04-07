import pandas as pd
import numpy as np
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
    list_scores = []

    for algorithm in CAMEL_TO_SNAKE.keys():
        scores = load_csv(f"page7_MultivariateXWASResults/Scores/Scores_{algorithm}_test.csv", index_col=0).drop(
            columns="subset"
        )
        scores.rename(columns={"env_dataset": "category", "organ": "dimension"}, inplace=True)

        scores_cleaned_dimension = scores.set_index("dimension").rename(index=DICT_TO_CHANGE_DIMENSIONS).reset_index()

        every_category = np.array(scores_cleaned_dimension["category"].tolist())
        category_to_split = ~scores_cleaned_dimension["category"].str.startswith("medical_diagnoses")

        every_category[category_to_split] = list(
            np.array(list(map(np.array, scores_cleaned_dimension["category"][category_to_split].str.split("_"))))[:, 1]
        )

        scores_cleaned_dimension["category"] = every_category
        scores_cleaned_dimension["algorithm"] = CAMEL_TO_SNAKE[algorithm]

        scores_cleaned = (
            scores_cleaned_dimension.set_index("category").rename(index=DICT_TO_CHANGE_CATEGORIES).reset_index()
        )

        list_scores.append(scores_cleaned)

    pd.concat(list_scores, ignore_index=True).to_feather("data/xwas/multivariate_results/scores.feather")