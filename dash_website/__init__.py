DIMENSIONS = sorted(
    [
        "set",
        "set_instances01",
        "set_instances1.5x",
        "set_instances23",
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
        "ImmuneSystem",
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
    "set": "*",
    "set_instances01": "*instances01",
    "set_instances1.5x": "*instances1.5x",
    "set_instances23": "*instances23",
}


ALL_BIOMARKERS = sorted(
    [
        "HandGripStrength",
        "BrainGreyMatterVolumes",
        "BrainSubcorticalVolumes",
        "HeartSize",
        "HeartPWA",
        "ECGAtRest",
        "AnthropometryImpedance",
        "UrineBiochemistry",
        "BloodBiochemistry",
        "BloodCount",
        "EyeAutorefraction",
        "EyeAcuity",
        "EyeIntraocularPressure",
        "BraindMRIWeightedMeans",
        "Spirometry",
        "BloodPressure",
        "AnthropometryBodySize",
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
ALL_PHENOTYPES = sorted(
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
    ALL_BIOMARKERS + ALL_PHENOTYPES + ALL_DISEASES + ALL_ENVIRONMENTAL + ALL_SOCIOECONOMICS + ["FamilyHistory"]
)

CATEGORIES = ["All", "Biomarkers", "Phenotypes", "Diseases", "Environmental", "Socioeconomics"]

MAIN_CATEGORIES_TO_CATEGORIES = {
    "All": ALL_CATEGORIES,
    "Biomarkers": ALL_BIOMARKERS,
    "Phenotypes": ALL_PHENOTYPES,
    "Diseases": ALL_DISEASES,
    "Environmental": ALL_ENVIRONMENTAL,
    "Socioeconomics": ALL_SOCIOECONOMICS,
}
