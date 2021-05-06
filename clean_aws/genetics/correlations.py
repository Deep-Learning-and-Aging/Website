import pandas as pd
from dash_website.utils.aws_loader import load_csv


COLUMNS_TO_TAKE = {
    "organ": "dimension",
    "view": "subdimension",
    "R-Squared_all": "r2",
    "R-Squared_sd_all": "r2_std",
}
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

    correlations_raw_ = load_csv("page17_GWASCorrelations/GWAS_correlations_Age.csv")
    correlations_raw = correlations_raw_.melt(
        id_vars=["Unnamed: 0"], value_vars=correlations_raw_.columns.drop("Unnamed: 0")
    ).rename(
        columns={
            "Unnamed: 0": "squeezed_dimensions_1",
            "variable": "squeezed_dimensions_2",
            "value": "correlation",
        }
    )

    correlations_std_raw_ = load_csv("page17_GWASCorrelations/GWAS_correlations_sd_Age.csv")
    correlations_std_raw = correlations_std_raw_.melt(
        id_vars=["Unnamed: 0"], value_vars=correlations_raw_.columns.drop("Unnamed: 0")
    ).rename(
        columns={
            "Unnamed: 0": "squeezed_dimensions_1",
            "variable": "squeezed_dimensions_2",
            "value": "correlation_std",
        }
    )

    heritability = load_csv("page11_GWASHeritability/Heritability/GWAS_heritabilities_Age.csv").rename(
        columns={"Organ": "squeezed_dimensions", "h2_sd": "h2_std"}
    )
    heritability.drop(
        index=heritability["squeezed_dimensions"][heritability["squeezed_dimensions"].isna()].index, inplace=True
    )
    heritability.set_index("squeezed_dimensions", inplace=True)

    correlations = pd.DataFrame(
        None,
        columns=[
            "squeezed_dimensions_1",
            "dimension_1",
            "subdimension_1",
            "r2_1",
            "r2_std_1",
            "heritability_1",
            "heritability_std_1",
            "squeezed_dimensions_2",
            "dimension_2",
            "subdimension_2",
            "r2_2",
            "r2_std_2",
            "heritability_2",
            "heritability_std_2",
            "correlation",
            "correlation_std",
        ],
    )

    for idx_dimensions in ["1", "2"]:
        correlations[f"squeezed_dimensions_{idx_dimensions}"] = correlations_raw[
            f"squeezed_dimensions_{idx_dimensions}"
        ]
        correlations.set_index(f"squeezed_dimensions_{idx_dimensions}", inplace=True)
        correlations[f"dimension_{idx_dimensions}"] = scores["dimension"]
        correlations[f"subdimension_{idx_dimensions}"] = scores["subdimension"]
        correlations[f"r2_{idx_dimensions}"] = scores["r2"]
        correlations[f"r2_std_{idx_dimensions}"] = scores["r2_std"]
        correlations[f"h2_{idx_dimensions}"] = heritability["h2"]
        correlations[f"h2_std_{idx_dimensions}"] = heritability["h2_std"]
        correlations.reset_index(inplace=True)

    correlations_raw.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
    correlations_std_raw.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
    correlations.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
    correlations["correlation"] = correlations_raw["correlation"]
    correlations["correlation_std"] = correlations_std_raw["correlation_std"]

    correlations.reset_index(drop=True).replace(DICT_TO_CHANGE_DIMENSIONS).to_feather(
        "all_data/genetics/correlations/correlations.feather"
    )
