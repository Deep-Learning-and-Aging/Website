from dash_website.utils.aws_loader import upload_file, load_feather, load_csv

SAMPLE_DEFINITION_NAMING = {"instances": "all_samples_per_participant", "eids": "average_per_participant"}
SELECTED_DIMENSIONS = {
    "withEnsembles": "all_dimensions",
    "tuned": "without_ensemble_models",
    "bestmodels": "custom_dimensions",
}
COLUMNS_TO_TAKE = {
    "organ": "dimension",
    "view": "subdimension",
    "transformation": "sub_subdimension",
    "architecture": "algorithm",
    "N_all": "sample_size",
    "RMSE_all": "rmse",
    "RMSE_sd_all": "rmse_std",
    "R-Squared_all": "r2",
    "R-Squared_sd_all": "r2_std",
    "C-Index_all": "c_index",
    "C-Index_sd_all": "c_index_std",
    "C-Index-difference_all": "c_index_difference",
    "C-Index-difference_sd_all": "c_index_difference_std",
}
DICT_TO_CHANGE_DIMENSIONS = {"ImmuneSystem": "BloodCells"}


if __name__ == "__main__":
    for sample_definition in ["eids", "instances"]:
        scores_with_ci = load_csv(
            f"page2_predictions/Performances/PERFORMANCES_withEnsembles_withCI_alphabetical_{sample_definition}_Age_test.csv"
        )[COLUMNS_TO_TAKE].rename(columns=COLUMNS_TO_TAKE)
        scores_with_ci.loc[
            (scores_with_ci["dimension"] == "Musculoskeletal") & (scores_with_ci["sub_subdimension"] == "MRI"),
            "sub_subdimension",
        ] = "DXA"
        scores_with_ci.replace(DICT_TO_CHANGE_DIMENSIONS, inplace=True)
        scores_with_ci.set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"], inplace=True)

        for dimensions_selection in ["withEnsembles", "tuned", "bestmodels"]:
            scores = load_feather(
                f"age_prediction_performances/scores_{SAMPLE_DEFINITION_NAMING[sample_definition]}_{SELECTED_DIMENSIONS[dimensions_selection]}.feather"
            ).set_index(["dimension", "subdimension", "sub_subdimension", "algorithm"])

            scores[["c_index", "c_index_std", "c_index_difference", "c_index_difference_std"]] = scores_with_ci.loc[
                scores.index, ["c_index", "c_index_std", "c_index_difference", "c_index_difference_std"]
            ]

            scores.reset_index().to_feather(
                f"all_data/age_prediction_performances/scores_withCI_{SAMPLE_DEFINITION_NAMING[sample_definition]}_{SELECTED_DIMENSIONS[dimensions_selection]}.feather"
            )
            upload_file(
                f"all_data/age_prediction_performances/scores_withCI_{SAMPLE_DEFINITION_NAMING[sample_definition]}_{SELECTED_DIMENSIONS[dimensions_selection]}.feather",
                f"age_prediction_performances/scores_withCI_{SAMPLE_DEFINITION_NAMING[sample_definition]}_{SELECTED_DIMENSIONS[dimensions_selection]}.feather",
            )
