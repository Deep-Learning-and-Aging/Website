import pandas as pd
from dash_website.utils.aws_loader import load_csv

COLUMNS_TO_TAKE = {
    "organ": "dimension",
    "view": "subdimension",
    "R-Squared_all": "r2",
    "R-Squared_sd_all": "r2_std",
}

DATA_TYPE_NAMING = {
    "instances": "all_samples_per_participant",
    "eids": "average_per_participant",
    "*": "all_samples_when_possible_otherwise_average",
}
DICT_TO_CHANGE_DIMENSIONS = {"ImmuneSystem": "BloodCells"}


if __name__ == "__main__":
    for sample_definition in ["instances", "eids"]:
        scores_raw = (
            load_csv(
                f"page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_{sample_definition}_Age_test.csv"
            )[COLUMNS_TO_TAKE]
            .rename(columns=COLUMNS_TO_TAKE)
            .set_index("dimension")
        )

        ensembles_scores_raw = (
            load_csv(
                f"page2_predictions/Performances/PERFORMANCES_withEnsembles_alphabetical_{sample_definition}_Age_test.csv"
            )[COLUMNS_TO_TAKE]
            .rename(columns=COLUMNS_TO_TAKE)
            .set_index(["dimension", "subdimension"])
        )
        ensembles_scores_raw["subdimension"] = ensembles_scores_raw.index.get_level_values("subdimension")

        if sample_definition == "instances":
            for dimension_to_correct in ["Hearing", "Lungs"]:
                scores_raw.loc[dimension_to_correct, ["subdimension", "r2", "r2_std"]] = ensembles_scores_raw.loc[
                    (dimension_to_correct, "*"), ["subdimension", "r2", "r2_std"]
                ].values[0]
        else:  # sample_definition == "eids"
            scores_raw.loc["ImmuneSystem", ["subdimension", "r2", "r2_std"]] = ensembles_scores_raw.loc[
                ("ImmuneSystem", "*"), ["subdimension", "r2", "r2_std"]
            ].values[0]

        scores = scores_raw.reset_index()
        scores["squeezed_dimensions"] = scores["dimension"] + scores["subdimension"].replace("*", "")
        scores.set_index("squeezed_dimensions", inplace=True)

        correlations_raw_ = load_csv(
            f"page4_correlations/ResidualsCorrelations/ResidualsCorrelations_bestmodels_{sample_definition}_Age_test.csv"
        )
        correlations_raw = correlations_raw_.melt(
            id_vars=["Unnamed: 0"], value_vars=correlations_raw_.columns.drop("Unnamed: 0")
        )
        correlations_raw.rename(
            columns={
                "Unnamed: 0": "squeezed_dimensions_1",
                "variable": "squeezed_dimensions_2",
                "value": "correlation",
            },
            inplace=True,
        )

        correlations_std_raw_ = load_csv(
            f"page4_correlations/ResidualsCorrelations/ResidualsCorrelations_bestmodels_sd_{sample_definition}_Age_test.csv"
        )
        correlations_std_raw = correlations_std_raw_.melt(
            id_vars=["Unnamed: 0"], value_vars=correlations_std_raw_.columns.drop("Unnamed: 0")
        )
        correlations_std_raw.rename(
            columns={
                "Unnamed: 0": "squeezed_dimensions_1",
                "variable": "squeezed_dimensions_2",
                "value": "correlation_std",
            },
            inplace=True,
        )

        correlations = pd.DataFrame(
            None,
            columns=[
                "squeezed_dimensions_1",
                "dimension_1",
                "subdimension_1",
                "r2_1",
                "r2_std_1",
                "squeezed_dimensions_2",
                "dimension_2",
                "subdimension_2",
                "r2_2",
                "r2_std_2",
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
            correlations.reset_index(inplace=True)

        correlations_raw.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
        correlations_std_raw.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
        correlations.set_index(["squeezed_dimensions_1", "squeezed_dimensions_2"], inplace=True)
        correlations["correlation"] = correlations_raw["correlation"]
        correlations["correlation_std"] = correlations_std_raw["correlation_std"]

        correlations.reset_index(drop=True).replace(DICT_TO_CHANGE_DIMENSIONS).to_feather(
            f"all_data/correlation_between_accelerated_aging_dimensions/custom_dimensions_{DATA_TYPE_NAMING[sample_definition]}.feather"
        )

    correlation_all_samples_per_participant = pd.read_feather(
        f"all_data/correlation_between_accelerated_aging_dimensions/custom_dimensions_all_samples_per_participant.feather"
    ).set_index(
        [
            "dimension_1",
            "subdimension_1",
            "dimension_2",
            "subdimension_2",
        ]
    )
    correlation_average_per_participant = pd.read_feather(
        f"all_data/correlation_between_accelerated_aging_dimensions/custom_dimensions_average_per_participant.feather"
    ).set_index(
        [
            "dimension_1",
            "subdimension_1",
            "dimension_2",
            "subdimension_2",
        ]
    )

    index_to_replace = correlation_all_samples_per_participant[
        correlation_all_samples_per_participant["correlation"].isna()
    ].index
    all_samples_when_possible_otherwise_average = correlation_all_samples_per_participant.copy()
    all_samples_when_possible_otherwise_average.loc[index_to_replace] = correlation_average_per_participant.loc[
        index_to_replace
    ]
    all_samples_when_possible_otherwise_average.reset_index().to_feather(
        f"all_data/correlation_between_accelerated_aging_dimensions/custom_dimensions_{DATA_TYPE_NAMING['*']}.feather"
    )