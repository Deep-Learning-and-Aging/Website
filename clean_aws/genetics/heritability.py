import pandas as pd
from dash_website.utils.aws_loader import load_csv

COLUMNS_TO_TAKE = {"organ": "dimension", "view": "subdimension", "R-Squared_all": "r2", "R-Squared_sd_all": "r2_std"}
DICT_TO_CHANGE_DIMENSIONS = {"ImmuneSystem": "BloodCells"}


if __name__ == "__main__":
    scores_raw = (
        load_csv(f"page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_instances_Age_test.csv")[
            COLUMNS_TO_TAKE
        ]
        .rename(columns=COLUMNS_TO_TAKE)
        .set_index("dimension")
    )

    ensembles_scores_raw = (
        load_csv(f"page2_predictions/Performances/PERFORMANCES_withEnsembles_alphabetical_instances_Age_test.csv")[
            COLUMNS_TO_TAKE
        ]
        .rename(columns=COLUMNS_TO_TAKE)
        .set_index(["dimension", "subdimension"])
    )
    ensembles_scores_raw["subdimension"] = ensembles_scores_raw.index.get_level_values("subdimension")

    for dimension_to_correct in ["Hearing", "Lungs"]:
        scores_raw.loc[dimension_to_correct, ["subdimension", "r2", "r2_std"]] = ensembles_scores_raw.loc[
            (dimension_to_correct, "*"), ["subdimension", "r2", "r2_std"]
        ].values[0]

    scores = scores_raw.reset_index()
    scores["squeezed_dimensions"] = scores["dimension"] + scores["subdimension"].replace("*", "")
    scores.set_index("squeezed_dimensions", inplace=True)

    heritability = load_csv("page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv").rename(
        columns={"Organ": "squeezed_dimensions", "h2_sd": "h2_std"}
    )
    heritability.drop(
        index=heritability["squeezed_dimensions"][heritability["squeezed_dimensions"].isna()].index, inplace=True
    )
    heritability.set_index("squeezed_dimensions", inplace=True)

    heritability[f"dimension"] = scores["dimension"]
    heritability[f"subdimension"] = scores["subdimension"]

    heritability.reset_index(drop=True).replace(DICT_TO_CHANGE_DIMENSIONS).to_feather(
        "all_data/genetics/heritability/heritability.feather"
    )
