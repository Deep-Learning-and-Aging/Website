import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather
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
    "ImmuneSystem",
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
    "set": [],
    "set_instances01": [],
    "set_instances1.5x": [],
    "set_instances23": [],
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
    "ImmuneSystem": [],
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
        ["dimension_1", "dimension_2", "category"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["category", "variable"]
    )

    list_indexes = []
    for idx_dimension_1, dimension_1 in enumerate(DIMENSIONS + ["MainDimensions", "SubDimensions"]):
        if dimension_1 in ["MainDimensions", "SubDimensions"]:
            dimensions_2 = ["average"]
        else:
            dimensions_2 = ["average"] + DIMENSIONS[idx_dimension_1 + 1 :]
        for dimension_2 in dimensions_2:
            for category in FULL_CATEGORY:
                list_indexes.append([dimension_1, dimension_2, category])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["dimension_1", "dimension_2", "category"])

    list_columns = []
    for correlation_type in ["pearson", "spearman", "number_variables"]:
        if correlation_type == "number_variables":
            observations = ["number_variables"]
        else:
            observations = ["mean", "std"]
        for observation in observations:
            list_columns.append([correlation_type, observation])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["correlation_type", "observation"])

    template_averages_correlations = pd.DataFrame(None, index=indexes, columns=columns)

    for subset_method in tqdm(["union", "intersection", "all"]):
        averages_correlations = template_averages_correlations.copy()
        averages_correlations[("number_variables", "number_variables")] = correlations_raw[
            (subset_method, "number_variables")
        ]

        for correlation_type in ["pearson", "spearman"]:
            averages_correlations[(correlation_type, "mean")] = correlations_raw[(subset_method, correlation_type)]

            correlations = correlations_raw[(subset_method, correlation_type)].swaplevel().swaplevel(i=0, j=1)

            for category in FULL_CATEGORY:
                correlations_category = correlations.loc[category]

                averages_correlations.loc[
                    ("MainDimensions", "average", category), (correlation_type, "mean")
                ] = correlations_category.loc[PAIRS_MAIN_DIMENSIONS].mean()
                averages_correlations.loc[
                    ("MainDimensions", "average", category), (correlation_type, "std")
                ] = correlations_category.loc[PAIRS_MAIN_DIMENSIONS].std()

                averages_correlations.loc[
                    ("SubDimensions", "average", category), (correlation_type, "mean")
                ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].mean()
                averages_correlations.loc[
                    ("SubDimensions", "average", category), (correlation_type, "std")
                ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].std()

                for dimension_1 in DIMENSIONS:
                    correlations_independant = correlations_category.loc[dimension_1].drop(
                        index=([dimension_1] + DIMENSIONS_TO_EXCLUDE[dimension_1])
                    )

                    averages_correlations.loc[
                        (dimension_1, "average", category), (correlation_type, "mean")
                    ] = correlations_independant.mean()
                    averages_correlations.loc[
                        (dimension_1, "average", category), (correlation_type, "std")
                    ] = correlations_independant.std()

        averages_correlations.columns = map(str, averages_correlations.columns.tolist())
        averages_correlations.reset_index().to_feather(
            f"data/xwas/univariate_correlations/averages_correlations_{subset_method}.feather"
        )
