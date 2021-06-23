import pandas as pd

SAMPLE_DEFINITION = {
    "all_samples_per_participant": "Participant and time of examination",
    "average_per_participant": "Participant (average across samples)",
}
DIMENSIONS_SELECTION = {
    "custom_dimensions": "Custom dimensions",
    "all_dimensions": "All dimensions",
    "without_ensemble_models": "Without ensemble models",
}

SCORES = {"r2": "R²", "rmse": "RMSE", "c_index": "C-index", "c_index_difference": "C-index difference"}

CUSTOM_DIMENSIONS = pd.MultiIndex.from_tuples(
    [
        ["*", "*", "*", "*"],
        ["*instances01", "*", "*", "*"],
        ["*instances1.5x", "*", "*", "*"],
        ["*instances23", "*", "*", "*"],
        ["Abdomen", "*", "*", "*"],
        ["Abdomen", "Liver", "*", "*"],
        ["Abdomen", "Pancreas", "*", "*"],
        ["Arterial", "*", "*", "*"],
        ["Arterial", "Carotids", "*", "*"],
        ["Arterial", "PulseWaveAnalysis", "*", "*"],
        ["Biochemistry", "*", "*", "*"],
        ["Biochemistry", "Blood", "*", "*"],
        ["Biochemistry", "Urine", "*", "*"],
        ["Brain", "*", "*", "*"],
        ["Brain", "Cognitive", "*", "*"],
        ["Brain", "MRI", "*", "*"],
        ["Eyes", "*", "*", "*"],
        ["Eyes", "All", "*", "*"],
        ["Eyes", "Fundus", "*", "*"],
        ["Eyes", "OCT", "*", "*"],
        ["Hearing", "HearingTest", "Scalars", "*"],
        ["Heart", "*", "*", "*"],
        ["Heart", "ECG", "TimeSeries", "*"],
        ["Heart", "MRI", "*", "*"],
        ["BloodCells", "*", "*", "*"],
        ["Lungs", "Spirometry", "*", "*"],
        ["Musculoskeletal", "*", "*", "*"],
        ["Musculoskeletal", "FullBody", "*", "*"],
        ["Musculoskeletal", "Hips", "*", "*"],
        ["Musculoskeletal", "Knees", "DXA", "*"],
        ["Musculoskeletal", "Scalars", "*", "*"],
        ["Musculoskeletal", "Spine", "*", "*"],
        ["PhysicalActivity", "*", "*", "*"],
    ],
    names=["dimension", "subdimension", "sub_subdimension", "algorithm"],
)
