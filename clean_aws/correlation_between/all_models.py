import pandas as pd
from dash_website.utils.aws_loader import load_csv

DATA_TYPE_NAMING = {
    "instances": "all_samples_per_participant",
    "eids": "average_per_participant",
    "*": "all_possible_samples",
}
COLUMNS_TO_TAKE = {
    "organ": "dimension",
    "view": "subdimension",
    "transformation": "sub_subdimension",
    "architecture": "algorithm",
    "R-Squared_all": "r2",
    "R-Squared_sd_all": "r2_std",
}


if __name__ == "__main__":
    for data_type in ["instances", "eids"]:
        correlations_raw_ = load_csv(
            f"page4_correlations/ResidualsCorrelations/ResidualsCorrelations_{data_type}_Age_test.csv"
        )
        correlations_std_raw_ = load_csv(
            f"page4_correlations/ResidualsCorrelations/ResidualsCorrelations_sd_{data_type}_Age_test.csv"
        )

        correlations_raw = correlations_raw_.melt(
            id_vars=["Unnamed: 0"], value_vars=correlations_raw_.columns.drop("Unnamed: 0")
        )
        correlations_raw.rename(
            columns={"Unnamed: 0": "dimensions_1", "variable": "dimensions_2", "value": "correlation"}, inplace=True
        )

        correlations_std_raw = correlations_std_raw_.melt(
            id_vars=["Unnamed: 0"], value_vars=correlations_std_raw_.columns.drop("Unnamed: 0")
        )
        correlations_std_raw.rename(
            columns={"Unnamed: 0": "dimensions_1", "variable": "dimensions_2", "value": "correlation"}, inplace=True
        )

        correlations = pd.DataFrame(
            None,
            columns=[
                "dimension_1",
                "subdimension_1",
                "sub_subdimension_1",
                "algorithm_1",
                "r2_1",
                "r2_std_1",
                "dimension_2",
                "subdimension_2",
                "sub_subdimension_2",
                "algorithm_2",
                "r2_2",
                "r2_std_2",
                "correlation",
                "correlation_std",
            ],
        )

        for dimension_index in ["1", "2"]:
            split_residual = correlations_raw[f"dimensions_{dimension_index}"].str.split("_")

            correlations[f"dimension_{dimension_index}"] = split_residual.apply(
                lambda list_information: list_information[0]
            )
            correlations[f"subdimension_{dimension_index}"] = split_residual.apply(
                lambda list_information: list_information[1]
            )
            correlations[f"sub_subdimension_{dimension_index}"] = split_residual.apply(
                lambda list_information: list_information[2]
            )
            correlations[f"algorithm_{dimension_index}"] = split_residual.apply(
                lambda list_information: list_information[3]
            )

        correlations["correlation"] = correlations_raw["correlation"]
        correlations["correlation_std"] = correlations_std_raw["correlation"]

        scores_raw = load_csv(
            f"page2_predictions/Performances/PERFORMANCES_withEnsembles_alphabetical_{data_type}_Age_test.csv"
        )[COLUMNS_TO_TAKE].rename(columns=COLUMNS_TO_TAKE)
        scores_raw.set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"], inplace=True)

        correlations.set_index(["dimension_1", "subdimension_1", "sub_subdimension_1", "algorithm_1"], inplace=True)
        correlations[["r2_1", "r2_std_1"]] = scores_raw[["r2", "r2_std"]]

        correlations.reset_index(inplace=True)
        correlations.set_index(["dimension_2", "subdimension_2", "sub_subdimension_2", "algorithm_2"], inplace=True)
        correlations[["r2_2", "r2_std_2"]] = scores_raw[["r2", "r2_std"]]

        correlations.reset_index().to_feather(
            f"all_data/correlation_between_accelerated_aging_dimensions/all_models_{DATA_TYPE_NAMING[data_type]}.feather"
        )
