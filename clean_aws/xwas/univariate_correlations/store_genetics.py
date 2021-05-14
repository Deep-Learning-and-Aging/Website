from dash_website.utils.aws_loader import load_feather, upload_file


if __name__ == "__main__":
    squeezed_dimensions = load_feather(
        "xwas/squeezed_dimensions_participant_and_time_of_examination.feather"
    ).set_index(["dimension", "subdimension"])

    genetics = load_feather("genetics/correlations/correlations.feather")[
        ["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "correlation"]
    ]

    for index_dimension in [1, 2]:
        genetics.set_index([f"dimension_{index_dimension}", f"subdimension_{index_dimension}"], inplace=True)
        genetics[f"squeezed_dimension_{index_dimension}"] = squeezed_dimensions["squeezed_dimensions"]
        genetics.reset_index(drop=True, inplace=True)

    genetics.to_feather("all_data/xwas/univariate_correlations/genetics.feather")
    upload_file(
        "all_data/xwas/univariate_correlations/genetics.feather", "xwas/univariate_correlations/genetics.feather"
    )
