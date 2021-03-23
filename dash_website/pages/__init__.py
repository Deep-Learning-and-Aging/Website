ORGANS = sorted(
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
ALL_ENVIRONMENTAL = sorted(
    ["Alcohol", "Diet", "EarlyLifeFactors", "ElectronicDevices", "Medication", "SunExposure", "Smoking"]
)
ALL_SOCIOECONOMICS = sorted(["Education", "Employment", "Household", "SocialSupport", "OtherSociodemographics"])
ALL_PHENOTYPES = sorted(
    [
        "Breathing",
        "CancerScreening",
        "ChestPain",
        "Claudication",
        "Eyesight",
        "GeneralHealth",
        "GeneralPain",
        "Hearing",
        "MentalHealth",
        "Mouth",
        "SexualFactors",
        "Sleep",
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
ALL = sorted(
    ALL_BIOMARKERS + ALL_ENVIRONMENTAL + ALL_SOCIOECONOMICS + ALL_PHENOTYPES + ALL_DISEASES + ["FamilyHistory"]
)
