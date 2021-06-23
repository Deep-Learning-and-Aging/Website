# Shared
AGING_RATE_LEGEND = {"accelerated": "Accelerated", "normal": "Normal", "decelerated": "Decelerated"}

# For scalars
TREE_SCALARS = {
    "Arterial": {
        "All": ["Scalars"],
        "BloodPressure": ["Scalars"],
        "Carotids": ["Scalars"],
        "PulseWaveAnalysis": ["Scalars"],
    },
    "Biochemistry": {"All": ["Scalars"], "Blood": ["Scalars"], "Urine": ["Scalars"]},
    "BloodCells": {"BloodCount": ["Scalars"]},
    "Brain": {
        "All": ["Scalars"],
        "Cognitive": [
            "AllScalars",
            "ReactionTime",
            "MatrixPatternCompletion",
            "TowerRearranging",
            "SymbolDigitSubstitution",
            "PairedAssociativeLearning",
            "ProspectiveMemory",
            "NumericMemory",
            "FluidIntelligence",
            "TrailMaking",
            "PairsMatching",
        ],
        "MRI": ["AllScalars", "dMRIWeightedMeans", "GreyMatterVolumes", "SubcorticalVolumes"],
    },
    "Eyes": {
        "Acuity": ["Scalars"],
        "All": ["Scalars"],
        "Autorefraction": ["Scalars"],
        "IntraocularPressure": ["Scalars"],
    },
    "Hearing": {"HearingTest": ["Scalars"]},
    "Heart": {"All": ["Scalars"], "ECG": ["Scalars"], "MRI": ["Size", "PulseWaveAnalysis", "AllScalars"]},
    "Lungs": {"Spirometry": ["Scalars"]},
    "Musculoskeletal": {
        "Scalars": ["AllScalars", "Anthropometry", "Impedance", "HeelBoneDensitometry", "HandGripStrength"]
    },
    "PhysicalActivity": {"FullWeek": ["Scalars"]},
}

FEATURES_TABLE_COLUMNS = {
    "feature": "Feature",
    "percentage_correlation": "Percentage Correlation",
    "percentage_elastic_net": "Percentage Elastic Net",
    "percentage_light_gbm": "Percentage Light GBM",
    "percentage_neural_network": "Percentage Neural Network",
}

FEATURES_CORRELATIONS_TABLE_COLUMNS = {
    "index": "",
    "percentage_correlation": "Percentage Correlation",
    "percentage_elastic_net": "Percentage Elastic Net",
    "percentage_light_gbm": "Percentage Light GBM",
    "percentage_neural_network": "Percentage Neural Network",
}


# For images
DISPLAY_MODE = ["Raw", "Gradcam", "Saliency"]
