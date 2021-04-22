import pandas as pd
from dash_website.utils.aws_loader import load_csv

columns_to_take = [
    "id",
    "sex",
    "age_category",
    "sample",
    "aging_rate",
    "Age",
    "Biological_Age",
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
]


if __name__ == "__main__":
    list_information = []

    for chamber_type in [3, 4]:
        information_raw = load_csv(
            f"page12_AttentionMapsVideos/RawVideos/files/AttentionMaps-samples_Age_Heart_MRI_{chamber_type}chambersRawVideo.csv",
            usecols=columns_to_take,
        )[columns_to_take].set_index("id")
        information_raw.drop(index=information_raw[information_raw["aging_rate"] != "normal"].index, inplace=True)

        information = pd.DataFrame(
            None,
            columns=["chamber", "sex", "age_group", "sample", "chronological_age", "biological_age", "ethnicity"],
            index=information_raw.index,
        )

        information["chamber"] = chamber_type
        information["sex"] = information_raw["sex"].str.lower()
        information["age_group"] = information_raw["age_category"]
        information["sample"] = information_raw["sample"]
        information["chronological_age"] = information_raw["Age"].round(1)
        information["biological_age"] = information_raw["Biological_Age"]

        for id_participant in information_raw.index:
            ethnicities = information_raw.loc[
                id_participant, information_raw.columns[information_raw.columns.str.startswith("Ethnicity")]
            ]

            information.loc[id_participant, "ethnicity"] = " ".join(
                list(map(lambda list_ethni: list_ethni.split(".")[1], ethnicities[ethnicities == 1].index))
            )

        list_information.append(information.reset_index())

    pd.concat(list_information).reset_index(drop=True).to_feather("all_data/datasets/videos/information.feather")