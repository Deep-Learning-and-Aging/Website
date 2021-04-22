# For time series
TREE_TIME_SERIES = {
    "Arterial": {"PulseWaveAnalysis": ["TimeSeries"]},
    "Heart": {"ECG": ["TimeSeries"]},
    "PhysicalActivity": {"FullWeek": ["Acceleration", "TimeSeriesFeatures"], "Walking": ["3D"]},
}

INFORMATION_TIME_SERIES = {
    "Arterial": {
        "PulseWaveAnalysis": {
            "TimeSeries": {
                "nb_channel": 1,
                "y_label": "blood pressure [normalized]",
                "x_label": "Time (10 min / unit)",
            }
        }
    },
    "Heart": {
        "ECG": {
            "TimeSeries": {
                "nb_channel": 12,
                "y_label": "5 uV / Lsb",
                "x_label": "Time (2 min / unit)",
            }
        }
    },
    "PhysicalActivity": {
        "FullWeek": {
            "Acceleration": {
                "nb_channel": 10080,
                "y_label": "miligravity",
                "x_label": "Time (1 min / unit)",
            },
            "TimeSeriesFeatures": {
                "nb_channel": 113,
                "y_label": "Acceleration",
                "x_label": "Time (5 min / unit)",
            },
        },
        "Walking": {
            "3D": {
                "nb_channel": 3,
                "y_label": "5 uV / Lsb",
                "x_label": "Time (2 min / unit)",
            }
        },
    },
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
