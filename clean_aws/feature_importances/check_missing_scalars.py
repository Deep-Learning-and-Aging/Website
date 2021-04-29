from tqdm import tqdm
import pandas as pd

from dash_website.utils.aws_loader import does_key_exists

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
    ("Demographics", "All", "Scalars"): "Demographics",
}

if __name__ == "__main__":
    missing_csvs_array = []

    for dimension, subdimension, sub_subdimension in tqdm(DIMENSION_TO_NAME.keys()):
        for target in ["age", "sex"]:
            for algorithm in ["correlation", "elastic_net", "light_gbm", "neural_network"]:
                for observation in ["mean", "std"]:
                    if observation == "mean":
                        observation_path = ""
                    else:
                        observation_path = "_sd"

                    if not does_key_exists(
                        f"page3_featureImp/FeatureImp/FeatureImp{observation_path}_{TARGET_NAMING[target]}_{dimension}_{subdimension}_{sub_subdimension}_{ALGORITHM_NAMING[algorithm]}.csv"
                    ):
                        missing_csvs_array.append(
                            [dimension, subdimension, sub_subdimension, target, algorithm, observation]
                        )
    missing_csvs = pd.DataFrame(
        missing_csvs_array,
        columns=["dimension", "subdimension", "sub_subdimension", "target", "algorithm", "observation"],
    )

    missing_csvs.to_excel("all_data/missing_feature_importances_scalars.xlsx")
