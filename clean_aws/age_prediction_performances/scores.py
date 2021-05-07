from dash_website.pages.tools import load_csv

SAMPLE_DEFINITION_NAMING = {
    "instances": "all_samples_per_participant",
    "eids": "average_per_participant",
    "*": "all_samples_when_possible_otherwise_average",
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
}
DICT_TO_CHANGE_DIMENSIONS = {"ImmuneSystem": "BloodCells"}
SELECTED_DIMENSIONS = {
    "withEnsembles": "all_dimensions",
    "tuned": "without_ensemble_models",
    "bestmodels": "custom_dimensions",
}


if __name__ == "__main__":
    for sample_definition in ["instances", "eids"]:
        for selected_dimensions in ["withEnsembles", "tuned", "bestmodels"]:
            scores = load_csv(
                f"page2_predictions/Performances/PERFORMANCES_{selected_dimensions}_alphabetical_{sample_definition}_Age_test.csv"
            )[COLUMNS_TO_TAKE].rename(columns=COLUMNS_TO_TAKE)
            scores.loc[
                (scores["dimension"] == "Musculoskeletal") & (scores["sub_subdimension"] == "MRI"), "sub_subdimension"
            ] = "DXA"
            scores.replace(DICT_TO_CHANGE_DIMENSIONS).to_feather(
                f"all_data/age_prediction_performances/scores_{SAMPLE_DEFINITION_NAMING[sample_definition]}_{SELECTED_DIMENSIONS[selected_dimensions]}.feather"
            )
