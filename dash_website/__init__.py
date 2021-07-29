import pandas as pd


RENAME_DIMENSIONS = {
    "*": "set",
    "*instances01": "set_instances01",
    "*instances1.5x": "set_instances1.5x",
    "*instances23": "set_instances23",
}


ALL_BIOMARKERS = sorted(
    [
        "HandGripStrength",
        "BrainGreyMatterVolumes",
        "BrainSubcorticalVolumes",
        "HeartFunction",
        "HeartPWA",
        "ECGAtRest",
        "Impedance",
        "UrineBiochemistry",
        "BloodBiochemistry",
        "BloodCount",
        "EyeAutorefraction",
        "EyeAcuity",
        "EyeIntraocularPressure",
        "BraindMRIWeightedMeans",
        "Spirometry",
        "BloodPressure",
        "Anthropometry",
        "ArterialStiffness",
        "CarotidUltrasound",
        "BoneDensitometryOfHeel",
        "HearingTest",
        "CognitiveFluidIntelligence",
        "CognitiveMatrixPatternCompletion",
        "CognitiveNumericMemory",
        "CognitivePairedAssociativeLearning",
        "CognitivePairsMatching",
        "CognitiveProspectiveMemory",
        "CognitiveReactionTime",
        "CognitiveSymbolDigitSubstitution",
        "CognitiveTowerRearranging",
        "CognitiveTrailMaking",
        "PhysicalActivity",
    ]
)
ALL_CLINICALPHENOTYPES = sorted(
    [
        "Breathing",
        "Claudication",
        "ChestPain",
        "CancerScreening",
        "Eyesight",
        "Hearing",
        "MentalHealth",
        "Mouth",
        "GeneralHealth",
        "GeneralPain",
        "SexualFactors",
    ]
)
ALL_DISEASES = [
    "medical_diagnoses_%s" % letter
    for letter in [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
]
ALL_ENVIRONMENTAL = sorted(
    [
        "Alcohol",
        "Diet",
        "ElectronicDevices",
        "Medication",
        "SunExposure",
        "EarlyLifeFactors",
        "Sleep",
        "Smoking",
        "PhysicalActivityQuestionnaire",
    ]
)
ALL_SOCIOECONOMICS = sorted(["Education", "Employment", "Household", "SocialSupport", "OtherSociodemographics"])

ALL_CATEGORIES = sorted(
    ALL_BIOMARKERS
    + ALL_CLINICALPHENOTYPES
    + ALL_DISEASES
    + ALL_ENVIRONMENTAL
    + ALL_SOCIOECONOMICS
    + ["FamilyHistory", "Genetics", "Phenotypic"]
)

CATEGORIES = ["All", "Biomarkers", "ClinicalPhenotypes", "Diseases", "Environmental", "Socioeconomics"]

MAIN_CATEGORIES_TO_CATEGORIES = {
    "All": ALL_CATEGORIES,
    "Biomarkers": ALL_BIOMARKERS,
    "ClinicalPhenotypes": ALL_CLINICALPHENOTYPES,
    "Diseases": ALL_DISEASES,
    "Environmental": ALL_ENVIRONMENTAL,
    "Socioeconomics": ALL_SOCIOECONOMICS,
}

ALGORITHMS = {
    "correlation": "Correlation",
    "best_algorithm": "Best Algorithm",
    "elastic_net": "Elastic Net",
    "light_gbm": "Light GBM",
    "neural_network": "Neural Network",
    "inception_res_net_v2": "Inception ResNet V2",
    "inception_v3": "Inception V3",
    "1dcnn": "1 DCNN",
    "3dcnn": "3 DCNN",
    "*": "*",
}

CORRELATION_TYPES = {"pearson": "Pearson", "spearman": "Spearman"}

DOWNLOAD_CONFIG = {"toImageButtonOptions": {"format": "svg"}}
GRAPH_SIZE = 1200

ORDER_TYPES = {"custom": "Custom", "clustering": "Clustering", "r2": "R²"}

CUSTOM_DIMENSIONS = pd.MultiIndex.from_tuples(
    [
        ("*", "*", "*", "*"),
        ("*instances01", "*", "*", "*"),
        ("*instances1.5x", "*", "*", "*"),
        ("*instances23", "*", "*", "*"),
        ("Brain", "*", "*", "*"),
        ("Brain", "Cognitive", "*", "*"),
        ("Brain", "MRI", "*", "*"),
        ("Eyes", "*", "*", "*"),
        ("Eyes", "All", "*", "*"),
        ("Eyes", "Fundus", "*", "*"),
        ("Eyes", "OCT", "*", "*"),
        ("Hearing", "HearingTest", "Scalars", "*"),
        ("Lungs", "Spirometry", "*", "*"),
        ("Arterial", "*", "*", "*"),
        ("Arterial", "Carotids", "*", "*"),
        ("Arterial", "PulseWaveAnalysis", "*", "*"),
        ("Heart", "*", "*", "*"),
        ("Heart", "ECG", "*", "*"),
        ("Heart", "MRI", "*", "*"),
        ("Abdomen", "*", "*", "*"),
        ("Abdomen", "Liver", "*", "*"),
        ("Abdomen", "Pancreas", "*", "*"),
        ("Musculoskeletal", "*", "*", "*"),
        ("Musculoskeletal", "FullBody", "*", "*"),
        ("Musculoskeletal", "Hips", "*", "*"),
        ("Musculoskeletal", "Knees", "DXA", "*"),
        ("Musculoskeletal", "Scalars", "*", "*"),
        ("Musculoskeletal", "Spine", "*", "*"),
        ("PhysicalActivity", "*", "*", "*"),
        ("Biochemistry", "*", "*", "*"),
        ("Biochemistry", "Blood", "*", "*"),
        ("Biochemistry", "Urine", "*", "*"),
        ("BloodCells", "BloodCount", "*", "*"),
    ],
    names=["dimension", "subdimension", "sub_subdimension", "algorithm"],
)

DIMENSIONS_SUBDIMENSIONS = dict(
    zip(
        list(
            map(
                lambda dimension: dimension.split("*")[0] if dimension[0] != "*" else dimension[:-1],
                ["".join(dimensions[:2]) for dimensions in CUSTOM_DIMENSIONS],
            )
        ),
        [" - ".join(dimensions[:2]) for dimensions in CUSTOM_DIMENSIONS],
    )
)
