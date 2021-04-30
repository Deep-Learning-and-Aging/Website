from dash_website.utils.aws_loader import load_csv

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

DATA_TYPE_NAMING = {"instances": "all_samples", "eids": "average_per_participant"}
ALGORITHMS_NAMING = {"ElasticNet": "elastic_net", "LightGBM": "light_gbm", "NeuralNetwork": "neural_network"}


for data_type in ["instances"]:  # ["eids", "instances"]:
    scores_raw = load_csv(f"page2_predictions/Performances/PERFORMANCES_tuned_alphabetical_{data_type}_Age_test.csv")

    scores = scores_raw[COLUMNS_TO_TAKE.keys()].rename(columns=COLUMNS_TO_TAKE)

    scores.drop(index=scores.index[~scores["algorithm"].isin(ALGORITHMS_NAMING.keys())]).replace(
        ALGORITHMS_NAMING
    ).reset_index(drop=True).to_feather(f"all_data/feature_importances/scores_{DATA_TYPE_NAMING[data_type]}.feather")
