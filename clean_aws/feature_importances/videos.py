from os import terminal_size
import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import copy_file, upload_file

COLUMNS_TO_TAKE = {
    "id": "id",
    "Sex": "sex",
    "age_category": "age_group",
    "aging_rate": "aging_rate",
    "Age": "chronological_age",
    "Pred": "biological_age",
}
SEX_NAME = {0.0: "female", 1.0: "male"}
SWAP_AGE_RATE = {"accelerated": "decelerated", "decelerated": "accelerated"}


if __name__ == "__main__":
    list_information = []

    for chamber in tqdm([3, 4]):
        information_raw = pd.read_csv(
            f"all_data/page12_AttentionMapsVideos/AttentionMapsVideos/AttentionMaps-samples_Age_Heart_MRI_{chamber}chambersRaw.csv"
        )
        information_raw["Sex"].replace(SEX_NAME, inplace=True)
        information_raw["aging_rate"].replace(SWAP_AGE_RATE, inplace=True)

        information = information_raw[COLUMNS_TO_TAKE].rename(columns=COLUMNS_TO_TAKE)
        information["chamber"] = chamber

        list_information.append(information)

        columns_for_storage = ["id", "Sex", "age_category", "aging_rate", "Gif", "Picture"]
        information_for_storage = information_raw[columns_for_storage].set_index("id")

        information_for_storage["name_gif"] = information_for_storage["Gif"].apply(lambda path: path.split("/")[-1])
        information_for_storage["name_picture"] = information_for_storage["Picture"].apply(
            lambda path: path.split("/")[-1]
        )

        for id_to_store in information_for_storage.drop(columns=["Gif", "Picture"]).index:
            old_key_gif = f"page12_AttentionMapsVideos/gif/{information_for_storage.loc[id_to_store, 'name_gif']}"
            new_key_gif = f"feature_importances/videos/{chamber}_chambers/{information_for_storage.loc[id_to_store, 'Sex']}/{information_for_storage.loc[id_to_store, 'age_category']}/{information_for_storage.loc[id_to_store, 'aging_rate']}.gif"

            # copy_file(old_key_gif, new_key_gif)

            old_key_jpg = f"page12_AttentionMapsVideos/img/{information_for_storage.loc[id_to_store, 'name_picture']}"
            new_key_jpg = f"feature_importances/videos/{chamber}_chambers/{information_for_storage.loc[id_to_store, 'Sex']}/{information_for_storage.loc[id_to_store, 'age_category']}/{information_for_storage.loc[id_to_store, 'aging_rate']}.jpg"

            # copy_file(old_key_jpg, new_key_jpg)

    pd.concat(list_information).reset_index(drop=True).to_feather(
        "all_data/feature_importances/videos/information.feather"
    )
    upload_file(
        "all_data/feature_importances/videos/information.feather", "feature_importances/videos/information.feather"
    )