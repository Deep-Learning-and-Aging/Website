import pandas as pd
from tqdm import tqdm

from dash_website.utils.aws_loader import load_feather, upload_file
from dash_website import DIMENSIONS, MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS


if __name__ == "__main__":
    every_feature = load_feather("xwas/multivariate_feature_importances/feature_importances.feather").set_index(
        ["dimension", "category"]
    )

    for dimension in tqdm(DIMENSIONS):
        for category in pd.Index(MAIN_CATEGORIES_TO_CATEGORIES["All"]).drop(
            ["Genetics", "Phenotypic", "PhysicalActivity"]
        ):
            every_feature.loc[(dimension, category)].reset_index(drop=True).to_feather(
                f"all_data/xwas/multivariate_feature_importances/dimension_category/features_{RENAME_DIMENSIONS.get(dimension, dimension)}_{category}.feather"
            )
            upload_file(
                f"all_data/xwas/multivariate_feature_importances/dimension_category/features_{RENAME_DIMENSIONS.get(dimension, dimension)}_{category}.feather",
                f"xwas/multivariate_feature_importances/dimension_category/features_{RENAME_DIMENSIONS.get(dimension, dimension)}_{category}.feather",
            )
