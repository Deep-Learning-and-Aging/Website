from tqdm import tqdm
import pandas as pd

from dash_website.utils.aws_loader import load_csv

ALGORITHM_NAMING = {
    "correlation": "Correlation",
    "elastic_net": "ElasticNet",
    "light_gbm": "LightGbm",
    "neural_network": "NeuralNetwork",
}

TARGET_NAMING = {"age": "Age", "sex": "Sex"}

DIMENSION_TO_NAME = {
    ("Brain", "MRI", "GreyMatterVolumes"): "BrainGreyMatterVolumes",
    ("Brain", "MRI", "SubcorticalVolumes"): "BrainSubcorticalVolumes",
    ("Brain", "MRI", "dMRIWeightedMeans"): "BraindMRIWeightedMeans",
    ("Brain", "MRI", "AllScalars"): "BrainMRIAllBiomarkers",
    ("Brain", "Cognitive", "ReactionTime"): "CognitiveReactionTime",
    ("Brain", "Cognitive", "MatrixPatternCompletion"): "CognitiveMatrixPatternCompletion",
    ("Brain", "Cognitive", "TowerRearranging"): "CognitiveTowerRearranging",
    ("Brain", "Cognitive", "SymbolDigitSubstitution"): "CognitiveSymbolDigitSubstitution",
    ("Brain", "Cognitive", "PairedAssociativeLearning"): "CognitivePairedAssociativeLearning",
    ("Brain", "Cognitive", "ProspectiveMemory"): "CognitiveProspectiveMemory",
    ("Brain", "Cognitive", "NumericMemory"): "CognitiveNumericMemory",
    ("Brain", "Cognitive", "FluidIntelligence"): "CognitiveFluidIntelligence",
    ("Brain", "Cognitive", "TrailMaking"): "CognitiveTrailMaking",
    ("Brain", "Cognitive", "PairsMatching"): "CognitivePairsMatching",
    ("Brain", "Cognitive", "AllScalars"): "CognitiveAllBiomarkers",
    ("Brain", "All", "Scalars"): "BrainAndCognitive",
    ("Eyes", "Autorefraction", "Scalars"): "EyeAutorefraction",
    ("Eyes", "Acuity", "Scalars"): "EyeAcuity",
    ("Eyes", "IntraocularPressure", "Scalars"): "EyeIntraocularPressure",
    ("Eyes", "All", "Scalars"): "EyesAllBiomarkers",
    ("Hearing", "HearingTest", "Scalars"): "HearingTest",
    ("Lungs", "Spirometry", "Scalars"): "Spirometry",
    ("Arterial", "BloodPressure", "Scalars"): "BloodPressure",
    ("Arterial", "Carotids", "Scalars"): "CarotidUltrasound",
    ("Arterial", "PWA", "Scalars"): "ArterialStiffness",
    ("Arterial", "All", "Scalars"): "VascularAllBiomarkers",
    ("Heart", "All", "Scalars"): "HeartAllBiomarkers",
    ("Heart", "MRI", "Size"): "HeartSize",
    ("Heart", "MRI", "PWA"): "HeartPWA",
    ("Heart", "MRI", "AllScalars"): "HeartMRIAll",
    ("Heart", "ECG", "Scalars"): "ECGAtRest",
    ("Musculoskeletal", "Scalars", "Impedance"): "AnthropometryImpedance",
    ("Musculoskeletal", "Scalars", "Anthropometry"): "AnthropometryBodySize",
    ("Musculoskeletal", "Scalars", "HeelBoneDensitometry"): "BoneDensitometryOfHeel",
    ("Musculoskeletal", "Scalars", "HandGripStrength"): "HandGripStrength",
    ("Musculoskeletal", "Scalars", "AllScalars"): "MusculoskeletalAllBiomarkers",
    ("Biochemistry", "Blood", "Scalars"): "BloodBiochemistry",
    ("Biochemistry", "Urine", "Scalars"): "UrineBiochemistry",
    ("Biochemistry", "All", "Scalars"): "Biochemistry",
    ("ImmuneSystem", "BloodCount", "Scalars"): "BloodCount",
    ("PhysicalActivity", "FullWeek", "Scalars"): "PhysicalActivity",
    # ("Demographics", "All", "Scalars"): "Demographics",
}


if __name__ == "__main__":
    for dimension, subdimension, sub_subdimension in tqdm(DIMENSION_TO_NAME.keys()):
        list_colums = []

        for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
            for observation in ["mean", "std"]:
                list_colums.append([algorithm, observation])
        columns = pd.MultiIndex.from_tuples(list_colums, names=["algorithm", "observation"])

        feature_for_index = load_csv(
            f"page3_featureImp/FeatureImp/FeatureImp_Age_{dimension}_{subdimension}_{sub_subdimension}_ElasticNet.csv"
        ).rename(columns={"features": "feature"})
        feature_for_index["feature"] = (
            feature_for_index["feature"].astype(str).apply(lambda feature: feature.split(".0")[0])
        )

        features = pd.DataFrame(None, columns=columns, index=feature_for_index["feature"])
        features.index.name = "feature"

        for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
            mean_feature = load_csv(
                f"page3_featureImp/FeatureImp/FeatureImp_Age_{dimension}_{subdimension}_{sub_subdimension}_{ALGORITHM_NAMING[algorithm]}.csv"
            ).rename(columns={"features": "feature"})
            mean_feature["feature"] = mean_feature["feature"].astype(str).apply(lambda feature: feature.split(".0")[0])
            mean_feature.set_index("feature", inplace=True)
            mean_feature.drop(index=mean_feature.index[mean_feature.index.duplicated()], inplace=True)

            std_feature = load_csv(
                f"page3_featureImp/FeatureImp/FeatureImp_sd_Age_{dimension}_{subdimension}_{sub_subdimension}_{ALGORITHM_NAMING[algorithm]}.csv"
            ).rename(columns={"features": "feature"})
            std_feature["feature"] = std_feature["feature"].astype(str).apply(lambda feature: feature.split(".0")[0])
            std_feature.set_index("feature", inplace=True)
            std_feature.drop(index=std_feature.index[std_feature.index.duplicated()], inplace=True)

            features[(algorithm, "mean")] = mean_feature["weight"] / mean_feature["weight"].abs().sum()
            features[(algorithm, "std")] = std_feature["weight"] / (mean_feature["weight"].abs().sum() ** 2)

        features.columns = map(str, features.columns.tolist())
        features.reset_index().to_feather(
            f"all_data/feature_importances/scalars/{dimension}_{subdimension}_{sub_subdimension}.feather"
        )
