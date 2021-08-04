from dash_website.utils.aws_loader import load_feather, load_csv
import pandas as pd


def formating_features():
    dimension, subdimension, sub_subdimension = "Heart", "MRI", "Size"

    RENAMING_COLUMNS = {
        "feature": "Feature",
        "percentage_correlation": "Correlation with age",
        "percentage_elastic_net": "Elastic Net",
        "percentage_light_gbm": "GBM",
        "percentage_neural_network": "Neural Network",
    }
    pd.read_csv(f"feature_importances/{dimension}_{subdimension}_{sub_subdimension}.csv").drop(
        columns=["Unnamed: 0"]
    ).rename(columns=RENAMING_COLUMNS).to_csv(
        f"feature_importances/cleaned/{dimension}_{subdimension}_{sub_subdimension}.csv"
    )


if __name__ == "__main__":
    new_features = (
        pd.read_csv("feature_importances/heart_size/HeartSize.csv")
        .rename(columns={"feature": "mean", "Unnamed: 0": "feature"})
        .set_index(["feature"])
    )

    new_indexes = list(new_features.index.str.split(".0").map(lambda list_: list_[0]))
    cleaned_indexes = []
    for new_index in new_indexes:
        if "Ethnicity" in new_index:
            if new_index.split("Ethnicity.")[1] == "NA":
                cleaned_indexes.append("nan")
            else:
                cleaned_indexes.append(new_index.split("Ethnicity.")[1])
        else:
            cleaned_indexes.append(new_index)

    new_features.index = cleaned_indexes

    dimension, subdimension, sub_subdimension = "Heart", "MRI", "Size"
    old_feature = load_feather(
        f"feature_importances/scalars/{dimension}_{subdimension}_{sub_subdimension}.feather"
    ).set_index("feature")

    old_feature[["('elastic_net', 'mean')", "('elastic_net', 'std')"]] = new_features
