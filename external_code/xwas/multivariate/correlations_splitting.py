from dash_website.utils.aws_loader import load_feather, upload_file
from dash_website import DIMENSIONS, RENAME_DIMENSIONS

SQUEEZED_DIMENSIONS = load_feather("xwas/squeezed_dimensions_participant_and_time_of_examination.feather").set_index(
    ["squeezed_dimensions"]
)


if __name__ == "__main__":
    correlations = load_feather("xwas/multivariate_correlations/correlations/correlations.feather")

    correlations.set_index(["dimension_1", "subdimension_1"], inplace=True)

    for squeezed_dimension in DIMENSIONS:
        dimension_1, subdimension_1 = SQUEEZED_DIMENSIONS.loc[squeezed_dimension, ["dimension", "subdimension"]]
        correlations.loc[(dimension_1, subdimension_1)].reset_index(drop=True).rename(
            columns={"dimension_2": "dimension", "subdimension_2": "subdimension"}
        ).to_feather(
            f"all_data/xwas/multivariate_correlations/correlations/dimensions/correlations_{RENAME_DIMENSIONS.get(squeezed_dimension, squeezed_dimension)}.feather"
        )
        upload_file(
            f"all_data/xwas/multivariate_correlations/correlations/dimensions/correlations_{RENAME_DIMENSIONS.get(squeezed_dimension, squeezed_dimension)}.feather",
            f"xwas/multivariate_correlations/correlations/dimensions/correlations_{RENAME_DIMENSIONS.get(squeezed_dimension, squeezed_dimension)}.feather",
        )

    correlations.reset_index(inplace=True)
    every_category = correlations["category"].drop_duplicates()

    correlations.set_index("category", inplace=True)
    SQUEEZED_DIMENSIONS.set_index(["dimension", "subdimension"], inplace=True)

    for category in every_category:
        correlations_category = correlations.loc[category].reset_index(drop=True)

        for index_dimension in [1, 2]:
            correlations_category.set_index(
                [f"dimension_{index_dimension}", f"subdimension_{index_dimension}"], inplace=True
            )
            correlations_category[f"r2_{index_dimension}"] = SQUEEZED_DIMENSIONS["r2"]
            correlations_category[f"r2_std_{index_dimension}"] = SQUEEZED_DIMENSIONS["r2_std"]
            correlations_category.reset_index(inplace=True)

        correlations_category.to_feather(
            f"all_data/xwas/multivariate_correlations/correlations/categories/correlations_{category}.feather"
        )
        upload_file(
            f"all_data/xwas/multivariate_correlations/correlations/categories/correlations_{category}.feather",
            f"xwas/multivariate_correlations/correlations/categories/correlations_{category}.feather",
        )
