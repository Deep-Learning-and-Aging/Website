# For time series
TREE_TIME_SERIES = {
    "Arterial": {"PulseWaveAnalysis": ["TimeSeries"]},
    "Heart": {"ECG": ["TimeSeries"]},
    "PhysicalActivity": {"FullWeek": ["Acceleration", "TimeSeriesFeatures"], "Walking": ["3D"]},
}


# For images
TREE_IMAGES = {
    "Abdomen": {"Liver": ["Raw", "Contrast"], "Pancreas": ["Raw", "Contrast"]},
    "Arterial": {"Carotids": ["CIMT120", "CIMT150", "LongAxis", "Mixed", "ShortAxis"]},
    "Brain": {
        "MRI": [
            "SagittalRaw",
            "SagittalReference",
            "CoronalRaw",
            "CoronalReference",
            "TransverseRaw",
            "TransverseReference",
        ]
    },
    "Eyes": {"Fundus": ["Raw"], "OCT": ["Raw"]},
    "Heart": {
        "MRI": [
            "2chambersRaw",
            "2chambersContrast",
            "3chambersRaw",
            "3chambersContrast",
            "4chambersRaw",
            "4chambersContrast",
        ]
    },
    "Musculoskeletal": {
        "FullBody": ["Figure", "Flesh", "Mixed", "Skeleton"],
        "Knees": ["DXA"],
        "Hips": ["DXA"],
        "Spine": ["Coronal", "Sagittal"],
    },
    "PhysicalActivity": {
        "FullWeek": [
            "GramianAngularField1minDifference",
            "GramianAngularField1minSummation",
            "MarkovTransitionField1min",
            "RecurrencePlots1min",
        ]
    },
}

SIDES_DIMENSION = ["Arterial", "Eyes", "Musculoskeletal"]
SIDES_SUBDIMENSION_EXCEPTION = ["FullBody", "Spine"]


# For videos
CHAMBERS_LEGEND = {"3": "3 chambers", "4": "4 chambers"}

SEX_LEGEND = {"male": "Male", "female": "Female"}

AGE_GROUP_LEGEND = {"young": "Young", "middle": "Middle", "old": "Old"}

SAMPLE_LEGEND = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9}

SEX_TO_PRONOUN = {"male": "his", "female": "her"}
