import pandas as pd


DIMENSIONS = sorted(
    [
        "*",
        "*instances01",
        "*instances1.5x",
        "*instances23",
        "Abdomen",
        "AbdomenLiver",
        "AbdomenPancreas",
        "Arterial",
        "ArterialPulseWaveAnalysis",
        "ArterialCarotids",
        "Biochemistry",
        "BiochemistryUrine",
        "BiochemistryBlood",
        "Brain",
        "BrainCognitive",
        "BrainMRI",
        "Eyes",
        "EyesAll",
        "EyesFundus",
        "EyesOCT",
        "Hearing",
        "HeartMRI",
        "Heart",
        "HeartECG",
        "BloodCells",
        "Lungs",
        "Musculoskeletal",
        "MusculoskeletalSpine",
        "MusculoskeletalHips",
        "MusculoskeletalKnees",
        "MusculoskeletalFullBody",
        "MusculoskeletalScalars",
        "PhysicalActivity",
    ]
)

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

ALGORITHMS_RENDERING = {
    "correlation": "Correlation",
    "best_algorithm": "Best Algorithm",
    "elastic_net": "Elastic Net",
    "light_gbm": "Light GBM",
    "neural_network": "Neural Network",
}

CORRELATION_TYPES = {"pearson": "Pearson", "spearman": "Spearman"}

DOWNLOAD_CONFIG = {"toImageButtonOptions": {"format": "svg"}}

ORDER_TYPES = {"custom": "Custom", "clustering": "Clustering", "r2": "R2"}

CUSTOM_ORDER = [
    "*",
    "*instances01",
    "*instances1.5x",
    "*instances23",
    "Brain",
    "Eyes",
    "Hearing",
    "Lungs",
    "Arterial",
    "Heart",
    "Abdomen",
    "Musculoskeletal",
    "PhysicalActivity",
    "Biochemistry",
    "BloodCells",
]

ORDER_DIMENSIONS = pd.MultiIndex.from_tuples(
    [
        ("*", "*"),
        ("*instances01", "*"),
        ("*instances1.5x", "*"),
        ("*instances23", "*"),
        ("Abdomen", "*"),
        ("Abdomen", "Liver"),
        ("Abdomen", "Pancreas"),
        ("Arterial", "*"),
        ("Arterial", "Carotids"),
        ("Arterial", "PulseWaveAnalysis"),
        ("Biochemistry", "*"),
        ("Biochemistry", "Blood"),
        ("Biochemistry", "Urine"),
        ("BloodCells", "*"),
        ("Brain", "*"),
        ("Brain", "Cognitive"),
        ("Brain", "MRI"),
        ("Eyes", "*"),
        ("Eyes", "All"),
        ("Eyes", "Fundus"),
        ("Eyes", "OCT"),
        ("Hearing", "*"),
        ("Heart", "*"),
        ("Heart", "ECG"),
        ("Heart", "MRI"),
        ("Lungs", "*"),
        ("Musculoskeletal", "*"),
        ("Musculoskeletal", "FullBody"),
        ("Musculoskeletal", "Hips"),
        ("Musculoskeletal", "Knees"),
        ("Musculoskeletal", "Scalars"),
        ("Musculoskeletal", "Spine"),
        ("PhysicalActivity", "*"),
    ]
)
