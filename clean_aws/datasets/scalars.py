from re import S, sub
from socket import CAN_RAW_RECV_OWN_MSGS
import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_csv

DIMENSION_TO_NAME = {
    # ("Brain", "MRI", "GreyMatterVolumes"): "BrainGreyMatterVolumes",
    # ("Brain", "MRI", "SubcorticalVolumes"): "BrainSubcorticalVolumes",
    # ("Brain", "MRI", "dMRIWeightedMeans"): "BraindMRIWeightedMeans",
    # ("Brain", "MRI", "AllScalars"): "BrainMRIAllBiomarkers",
    # ("Brain", "Cognitive", "ReactionTime"): "CognitiveReactionTime",
    # ("Brain", "Cognitive", "MatrixPatternCompletion"): "CognitiveMatrixPatternCompletion",
    # ("Brain", "Cognitive", "TowerRearranging"): "CognitiveTowerRearranging",
    # ("Brain", "Cognitive", "SymbolDigitSubstitution"): "CognitiveSymbolDigitSubstitution",
    # ("Brain", "Cognitive", "PairedAssociativeLearning"): "CognitivePairedAssociativeLearning",
    # ("Brain", "Cognitive", "ProspectiveMemory"): "CognitiveProspectiveMemory",
    # ("Brain", "Cognitive", "NumericMemory"): "CognitiveNumericMemory",
    # ("Brain", "Cognitive", "FluidIntelligence"): "CognitiveFluidIntelligence",
    # ("Brain", "Cognitive", "TrailMaking"): "CognitiveTrailMaking",
    # ("Brain", "Cognitive", "PairsMatching"): "CognitivePairsMatching",
    # ("Brain", "Cognitive", "AllScalars"): "CognitiveAllBiomarkers",
    # ("Brain", "All", "Scalars"): "BrainAndCognitive",
    # ("Eyes", "Autorefraction", "Scalars"): "EyeAutorefraction",
    # ("Eyes", "Acuity", "Scalars"): "EyeAcuity",
    # ("Eyes", "IntraocularPressure", "Scalars"): "EyeIntraocularPressure",
    # ("Eyes", "All", "Scalars"): "EyesAllBiomarkers",
    # ("Hearing", "HearingTest", "Scalars"): "HearingTest",
    # ("Lungs", "Spirometry", "Scalars"): "Spirometry",
    # ("Arterial", "BloodPressure", "Scalars"): "BloodPressure",
    # ("Arterial", "Carotids", "Scalars"): "CarotidUltrasound",
    # ("Arterial", "PWA", "Scalars"): "ArterialStiffness",
    # ("Arterial", "All", "Scalars"): "VascularAllBiomarkers",
    # ("Heart", "All", "Scalars"): "HeartAllBiomarkers",
    # ("Heart", "MRI", "Size"): "HeartSize",
    # ("Heart", "MRI", "PWA"): "HeartPWA",
    # ("Heart", "MRI", "AllScalars"): "HeartMRIAll",
    # ("Heart", "ECG", "Scalars"): "ECGAtRest",
    # ("Musculoskeletal", "Scalars", "Impedance"): "AnthropometryImpedance",
    # ("Musculoskeletal", "Scalars", "Anthropometry"): "AnthropometryBodySize",
    # ("Musculoskeletal", "Scalars", "HeelBoneDensitometry"): "BoneDensitometryOfHeel",
    # ("Musculoskeletal", "Scalars", "HandGripStrength"): "HandGripStrength",
    # ("Musculoskeletal", "Scalars", "AllScalars"): "MusculoskeletalAllBiomarkers",
    # ("Biochemistry", "Blood", "Scalars"): "BloodBiochemistry",
    # ("Biochemistry", "Urine", "Scalars"): "UrineBiochemistry",
    # ("Biochemistry", "All", "Scalars"): "Biochemistry",
    # ("ImmuneSystem", "BloodCount", "Scalars"): "BloodCount",
    ("PhysicalActivity", "FullWeek", "Scalars"): "PhysicalActivity",
    # ("Demographics", "All", "Scalars"): "Demographics",
}


if __name__ == "__main__":
    for dimension, subdimension, sub_subdimension in tqdm(DIMENSION_TO_NAME.keys()):
        print(dimension, subdimension, sub_subdimension)

        name = DIMENSION_TO_NAME[(dimension, subdimension, sub_subdimension)]

        if dimension == "ImmuneSystem":
            new_dimension = "BloodCells"
        else:
            new_dimension = dimension

        if dimension != "PhysicalActivity":
            raw_scalars = load_csv(f"page1_biomarkers/BiomarkerDatasets/{name}_ethnicity.csv").set_index("id")
        else:
            raw_scalars = load_csv(f"page1_biomarkers/BiomarkerDatasets/{name}_short.csv").set_index("id")

        rename_columns = {"Sex": "sex", "Age when attended assessment centre": "chronological_age"}

        for feature in raw_scalars.columns[raw_scalars.columns.str.contains(".0")]:
            rename_columns[feature] = feature.replace(".0", "")

        scalars = pd.DataFrame(None, index=raw_scalars.index, columns=list(rename_columns.keys()))

        scalars[list(rename_columns.keys())] = raw_scalars[list(rename_columns.keys())]

        if (dimension, subdimension, sub_subdimension) == ("PhysicalActivity", "FullWeek", "Scalars"):
            columns_ethinicities = (
                raw_scalars.columns[raw_scalars.columns.str.startswith("Ethnicity")]
                .to_series()
                .apply(lambda column: column.split(".")[1])
                .values
            )

            scalars[columns_ethinicities] = raw_scalars[
                raw_scalars.columns[raw_scalars.columns.str.startswith("Ethnicity")]
            ]

            columns_others = raw_scalars.columns[
                ~(
                    raw_scalars.columns.isin(list(rename_columns.keys()) + ["eid"])
                    | raw_scalars.columns.str.contains("_r")
                    | raw_scalars.columns.str.startswith("Ethnicity")
                )
            ]
            scalars[columns_others] = raw_scalars[columns_others]

        else:
            columns_ethinicities_and_others = raw_scalars.columns[
                ~(
                    raw_scalars.columns.isin(list(rename_columns.keys()) + ["eid"])
                    | raw_scalars.columns.str.contains("_r")
                )
            ]
            scalars[columns_ethinicities_and_others] = raw_scalars[columns_ethinicities_and_others]

        if (dimension, subdimension, sub_subdimension) == ("Arterial", "All", "Scalars"):
            change_second_pulse_rate = scalars.rename(columns=rename_columns).columns.tolist()
            change_second_pulse_rate[
                scalars.rename(columns=rename_columns).columns.duplicated().argmax()
            ] = "Pulse rate.0"

            scalars.columns = change_second_pulse_rate

            scalars.reset_index().to_feather(
                f"all_data/datasets/scalars/{new_dimension}_{subdimension}_{sub_subdimension}.feather"
            )
        else:
            scalars.rename(columns=rename_columns).reset_index().to_feather(
                f"all_data/datasets/scalars/{new_dimension}_{subdimension}_{sub_subdimension}.feather"
            )
