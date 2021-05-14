import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather, upload_file
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES


MAIN_DIMENSIONS = [
    "Abdomen",
    "Musculoskeletal",
    "Lungs",
    "Eyes",
    "Heart",
    "Arterial",
    "Brain",
    "Biochemistry",
    "Hearing",
    "BloodCells",
    "PhysicalActivity",
]

PAIRS_MAIN_DIMENSIONS = [
    [main_dim_1, main_dim_2]
    for idx_dim, main_dim_1 in enumerate(MAIN_DIMENSIONS)
    for main_dim_2 in MAIN_DIMENSIONS[idx_dim + 1 :]
]

PAIRS_SUBDIMENSIONS = [
    ["BrainMRI", "BrainCognitive"],
    ["EyesOCT", "EyesFundus"],
    ["HeartECG", "HeartMRI"],
    ["AbdomenLiver", "AbdomenPancreas"],
    ["BiochemistryBlood", "BiochemistryUrine"],
    ["MusculoskeletalScalars", "MusculoskeletalFullBody"],
    ["MusculoskeletalScalars", "MusculoskeletalSpine"],
    ["MusculoskeletalScalars", "MusculoskeletalHips"],
    ["MusculoskeletalScalars", "MusculoskeletalKnees"],
    ["MusculoskeletalFullBody", "MusculoskeletalSpine"],
    ["MusculoskeletalFullBody", "MusculoskeletalHips"],
    ["MusculoskeletalFullBody", "MusculoskeletalKnees"],
    ["MusculoskeletalSpine", "MusculoskeletalHips"],
    ["MusculoskeletalSpine", "MusculoskeletalKnees"],
    ["MusculoskeletalHips", "MusculoskeletalKnees"],
]
DIMENSIONS_TO_EXCLUDE = {
    "*": [],
    "*instances01": [],
    "*instances1.5x": [],
    "*instances23": [],
    "Abdomen": ["AbdomenLiver", "AbdomenPancreas"],
    "AbdomenLiver": ["Abdomen"],
    "AbdomenPancreas": ["Abdomen"],
    "Arterial": ["ArterialCarotids", "ArterialPulseWaveAnalysis"],
    "ArterialCarotids": ["Arterial"],
    "ArterialPulseWaveAnalysis": ["Arterial"],
    "Biochemistry": ["BiochemistryBlood", "BiochemistryUrine"],
    "BiochemistryBlood": ["Biochemistry"],
    "BiochemistryUrine": ["Biochemistry"],
    "Brain": ["BrainCognitive", "BrainMRI"],
    "BrainCognitive": ["Brain"],
    "BrainMRI": ["Brain"],
    "Eyes": ["EyesAll", "EyesFundus", "EyesOCT"],
    "EyesAll": ["Eyes"],
    "EyesFundus": ["Eyes"],
    "EyesOCT": ["Eyes"],
    "Hearing": [],
    "Heart": ["HeartECG", "HeartMRI"],
    "HeartECG": ["Heart"],
    "HeartMRI": ["Heart"],
    "BloodCells": [],
    "Lungs": [],
    "Musculoskeletal": [
        "MusculoskeletalFullBody",
        "MusculoskeletalHips",
        "MusculoskeletalKnees",
        "MusculoskeletalScalars",
        "MusculoskeletalSpine",
    ],
    "MusculoskeletalFullBody": ["Musculoskeletal"],
    "MusculoskeletalHips": ["Musculoskeletal"],
    "MusculoskeletalKnees": ["Musculoskeletal"],
    "MusculoskeletalScalars": ["Musculoskeletal"],
    "MusculoskeletalSpine": ["Musculoskeletal"],
    "PhysicalActivity": [],
}

FULL_CATEGORY = (
    MAIN_CATEGORIES_TO_CATEGORIES["All"]
    + ["Phenotypic", "Genetics"]
    + [f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()]
)


if __name__ == "__main__":
    correlations_raw = load_feather(f"xwas/univariate_correlations/correlations.feather").set_index(
        ["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "category"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations_raw.reset_index(inplace=True)
    for index_dimension in [1, 2]:
        correlations_raw[f"squeezed_dimension_{index_dimension}"] = correlations_raw[
            f"dimension_{index_dimension}"
        ] + correlations_raw[f"subdimension_{index_dimension}"].replace("*", "")
    correlations_raw = correlations_raw.drop(
        columns=["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"]
    ).set_index(["category", "squeezed_dimension_1", "squeezed_dimension_2"])

    list_indexes = []
    for dimension in DIMENSIONS + ["MainDimensions", "SubDimensions"]:
        for category in FULL_CATEGORY:
            list_indexes.append([dimension, category])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["dimension", "category"])

    list_columns = []
    for subset_method in ["all", "union", "intersection"]:
        for correlation_type in ["pearson", "spearman"]:
            for observation in ["mean", "std"]:
                list_columns.append([subset_method, correlation_type, observation])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["subset_method", "correlation_type", "observation"])

    averages_correlations = pd.DataFrame(None, index=indexes, columns=columns)

    for subset_method in tqdm(["union", "intersection", "all"]):
        for correlation_type in ["pearson", "spearman"]:
            for category in FULL_CATEGORY:
                correlations_category = correlations_raw.loc[category, (subset_method, correlation_type)]

                averages_correlations.loc[
                    ("MainDimensions", category), (subset_method, correlation_type, "mean")
                ] = correlations_category.loc[PAIRS_MAIN_DIMENSIONS].mean()
                averages_correlations.loc[
                    ("MainDimensions", category), (subset_method, correlation_type, "std")
                ] = correlations_category.loc[PAIRS_MAIN_DIMENSIONS].std()

                averages_correlations.loc[
                    ("SubDimensions", category), (subset_method, correlation_type, "mean")
                ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].mean()
                averages_correlations.loc[
                    ("SubDimensions", category), (subset_method, correlation_type, "std")
                ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].std()

                for dimension in DIMENSIONS:
                    correlations_independant = correlations_category.loc[dimension].drop(
                        index=([dimension] + DIMENSIONS_TO_EXCLUDE[dimension])
                    )

                    averages_correlations.loc[
                        (dimension, category), (subset_method, correlation_type, "mean")
                    ] = correlations_independant.mean()
                    averages_correlations.loc[
                        (dimension, category), (subset_method, correlation_type, "std")
                    ] = correlations_independant.std()

    averages_correlations.columns = map(str, averages_correlations.columns.tolist())
    averages_correlations.reset_index().to_feather(
        "all_data/xwas/univariate_correlations/averages_correlations.feather"
    )
    upload_file(
        "all_data/xwas/univariate_correlations/averages_correlations.feather",
        "xwas/univariate_correlations/averages_correlations.feather",
    )
