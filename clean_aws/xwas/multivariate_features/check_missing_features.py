import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import list_dir
from dash_website import DIMENSIONS, ALL_CATEGORIES


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


if __name__ == "__main__":
    list_indexes = []
    for category in ALL_CATEGORIES:
        for dimension in DIMENSIONS:
            for algorithm in ["ElasticNet", "LightGbm", "NeuralNetwork", "Correlation"]:
                list_indexes.append([category, dimension, algorithm])

    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["category", "dimension", "algorithm"])
    features = pd.Series(False, index=indexes, name="Exists")

    list_objects = list_dir("page18_MultivariateXWASFeatures/")

    for object_ in tqdm(list_objects):
        algorithm = object_.split("/")[-1][11:-4].split("_")[-1]  # [: -4] for ., c, s, v
        dimension = object_.split("/")[-1][11:-4].split("_")[-2]

        if "medical" in object_:
            category = f"medical_diagnoses_{object_.split('/')[-1][11:-4].split('_')[-3]}"
        else:
            category = object_.split("/")[-1][11:-4].split("_")[-3]

        features.loc[
            (
                DICT_TO_CHANGE_CATEGORIES.get(category, category),
                DICT_TO_CHANGE_DIMENSIONS.get(dimension, dimension),
                algorithm,
            )
        ] = True

    if (~features).sum() == 0:
        print("\n\n Every file is in AWS S3 for Linear XWAS Results ! \n\n")
    else:
        features[features == False].to_excel("missing_in_aws.xlsx")