from dash_website.utils.aws_loader import load_feather, upload_file


if __name__ == "__main__":
    squeezed_dimensions = load_feather(
        "xwas/squeezed_dimensions_participant_and_time_of_examination.feather"
    ).set_index(["dimension", "subdimension"])

    phenotypic = load_feather(
        "correlation_between_accelerated_aging_dimensions/custom_dimensions_all_samples_when_possible_otherwise_average.feather"
    )[["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "correlation"]]

    for index_dimension in [1, 2]:
        phenotypic.set_index([f"dimension_{index_dimension}", f"subdimension_{index_dimension}"], inplace=True)
        phenotypic[f"squeezed_dimension_{index_dimension}"] = squeezed_dimensions["squeezed_dimensions"]
        phenotypic.reset_index(drop=True, inplace=True)

    phenotypic.to_feather("all_data/xwas/univariate_correlations/phenotypic.feather")
    upload_file(
        "all_data/xwas/univariate_correlations/phenotypic.feather", "xwas/univariate_correlations/phenotypic.feather"
    )
