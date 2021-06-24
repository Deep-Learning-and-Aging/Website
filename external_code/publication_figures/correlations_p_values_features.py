import pandas as pd
from dash_website.utils.aws_loader import load_feather
import scipy.stats


dimension = "Heart"
subdimensions = {"All": ["Scalars"], "ECG": ["Scalars"], "MRI": ["Size", "PulseWaveAnalysis", "AllScalars"]}!!!!


if __name__ == "__main__":
    list_indexes = []
    for subdimension in subdimensions.keys():
        for sub_subdimension in subdimensions[subdimension]:
            list_indexes.append([subdimension, sub_subdimension])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["subdimension", "sub_subdimension"])

    p_values = pd.DataFrame(None, index=indexes, columns=["correlation_vs_elastic_net", "correlation_vs_light_gbm", "correlation_vs_neural_network", "elastic_net_vs_light_gbm","elastic_net_vs_neural_network", "light_gbm_vs_neural_network"])
    correlations = pd.DataFrame(None, index=indexes, columns=["correlation_vs_elastic_net", "correlation_vs_light_gbm", "correlation_vs_neural_network", "elastic_net_vs_light_gbm","elastic_net_vs_neural_network", "light_gbm_vs_neural_network"])

    for subdimension, sub_subdimension in p_values.index:
        features = load_feather(f"feature_importances/scalars/Heart_{subdimension}_{sub_subdimension}.feather").set_index("feature")
        features.columns = pd.MultiIndex.from_tuples(
            list(map(eval, features.columns.tolist())), names=["algorithm", "observation"]
        )
        for comparison in p_values.columns:
            algorithm_1, algorithm_2 = comparison.split("_vs_")

            correlation, p_value = scipy.stats.spearmanr(features[(algorithm_1, "mean")].abs(), features[(algorithm_2, "mean")].abs())
                    
            correlations.loc[(subdimension, sub_subdimension), comparison] = correlation
            p_values.loc[(subdimension, sub_subdimension), comparison] = p_value

    RENAMING_COLUMNS = {"correlation_vs_elastic_net": "Correlation vs. Elastic Net", "correlation_vs_light_gbm": "Correlation vs. GBM", "correlation_vs_neural_network": "Correlation vs. Neural Network", "elastic_net_vs_light_gbm": "Elastic Net vs. GBM","elastic_net_vs_neural_network": "Elastic Net vs. Neural Network", "light_gbm_vs_neural_network": "GBM vs. Neural Network", "subdimension": "Heart dimension", "sub_subdimension": "Subdimension"}
    RENAMING = {"All": "All Scalars", "Size": "Function", "PulseWaveAnalysis": "Pulse Wave Analysis", "AllScalars": "All MRI Scalars"}
    
    correlations.astype(float).round(3).reset_index().rename(columns=RENAMING_COLUMNS).replace(RENAMING).loc[[0, 2, 3, 4, 1]].reset_index(drop=True).to_csv("correlations_heart_spearman.csv")
    p_values.astype(float).round(3).reset_index().rename(columns=RENAMING_COLUMNS).replace(RENAMING).loc[[0, 2, 3, 4, 1]].reset_index(drop=True).to_csv("p_values_heart_spearman.csv")

    correlations.astype(float).round(3).reset_index().rename(columns=RENAMING_COLUMNS).replace(RENAMING).loc[[0, 2, 3, 4, 1]].reset_index(drop=True)