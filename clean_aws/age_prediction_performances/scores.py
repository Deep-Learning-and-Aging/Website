from dash_website.utils.aws_loader import load_csv, upload_file
import numpy as np


SAMPLE_DEFINITION_NAMING = {
    "instances": "all_samples_per_participant",
    "eids": "average_per_participant",
}
COLUMNS_TO_TAKE = {
    "organ": "dimension",
    "view": "subdimension",
    "transformation": "sub_subdimension",
    "architecture": "algorithm",
    "N_all": "sample_size",
    "R-Squared_str_all": "r2_and_std",
    "C-Index_str_all": "c_index_and_std",
    "RMSE_str_all": "rmse_and_std",
    "C-Index-difference_str_all": "c_index_difference_and_std",
}
DICT_TO_CHANGE_DIMENSIONS = {
    "ImmuneSystem": "BloodCells",
    "InceptionResNetV2": "inception_res_net_v2",
    "InceptionV3": "inception_v3",
    "ElasticNet": "elastic_net",
    "LightGBM": "light_gbm",
    "NeuralNetwork": "neural_network",
    "1DCNN": "1dcnn",
    "3DCNN": "3dcnn",
}


if __name__ == "__main__":
    for sample_definition in ["instances", "eids"]:
        scores = load_csv(
            f"page2_predictions/Performances/PERFORMANCES_withEnsembles_withCI_alphabetical_{sample_definition}_Age_test.csv"
        )[COLUMNS_TO_TAKE].rename(columns=COLUMNS_TO_TAKE)

        for metric in ["r2", "rmse", "c_index", "c_index_difference"]:
            scores[metric] = scores[f"{metric}_and_std"].str.split("+", expand=True)[0].astype(np.float32)
            scores[f"{metric}_std"] = (
                scores[f"{metric}_and_std"]
                .str.split("+", expand=True)[1]
                .str.split("-", expand=True)[1]
                .astype(np.float32)
            )

            scores.drop(columns=f"{metric}_and_std", inplace=True)

        scores.loc[
            (scores["dimension"] == "Musculoskeletal") & (scores["sub_subdimension"] == "MRI"), "sub_subdimension"
        ] = "DXA"
        scores.replace(DICT_TO_CHANGE_DIMENSIONS).to_feather(
            f"all_data/age_prediction_performances/scores_{SAMPLE_DEFINITION_NAMING[sample_definition]}.feather"
        )
        upload_file(
            f"all_data/age_prediction_performances/scores_{SAMPLE_DEFINITION_NAMING[sample_definition]}.feather",
            f"age_prediction_performances/scores_{SAMPLE_DEFINITION_NAMING[sample_definition]}.feather",
        )
