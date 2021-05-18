from tqdm import tqdm

from dash_website.utils.aws_loader import load_csv, load_feather, upload_file
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, CATEGORIES


EVERY_CATEGORIES = [f"All_{main_category}" for main_category in CATEGORIES] + MAIN_CATEGORIES_TO_CATEGORIES["All"]

if __name__ == "__main__":
    squeezed_dimensions = (
        load_csv(f"page2_predictions/Performances/PERFORMANCES_bestmodels_alphabetical_instances_Age_test.csv")[
            ["organ", "view", "R-Squared_all", "R-Squared_sd_all"]
        ]
        .rename(
            columns={"organ": "dimension", "view": "subdimension", "R-Squared_all": "r2", "R-Squared_sd_all": "r2_std"}
        )
        .replace({"ImmuneSystem": "BloodCells"})
        .set_index("dimension")
    )
    squeezed_dimensions.loc["Lungs", "subdimension"] = "*"
    squeezed_dimensions.loc["Hearing", "subdimension"] = "*"
    squeezed_dimensions.reset_index(inplace=True)
    squeezed_dimensions["squeezed_dimensions"] = squeezed_dimensions["dimension"] + squeezed_dimensions[
        "subdimension"
    ].replace("*", "")
    squeezed_dimensions["squeezed_dimensions"].replace(
        {
            "*": "set",
            "*instances01": "set_instances01",
            "*instances1.5x": "set_instances1.5x",
            "*instances23": "set_instances23",
        },
        inplace=True,
    )
    squeezed_dimensions.set_index("squeezed_dimensions", inplace=True)

    every_correlation = load_feather(f"xwas/univariate_correlations/correlations/correlations.feather").set_index(
        "category"
    )

    for category in tqdm(EVERY_CATEGORIES):
        correlations = (
            every_correlation.loc[category]
            .reset_index(drop=True)
            .rename(columns={"dimension_1": "dimensions_1", "dimension_2": "dimensions_2"})
        )

        for idx_dimension in ["1", "2"]:
            correlations.set_index(f"dimensions_{idx_dimension}", inplace=True)
            correlations[f"dimension_{idx_dimension}"] = squeezed_dimensions["dimension"]
            correlations[f"subdimension_{idx_dimension}"] = squeezed_dimensions["subdimension"]
            correlations[f"r2_{idx_dimension}"] = squeezed_dimensions["r2"]
            correlations[f"r2_std_{idx_dimension}"] = squeezed_dimensions["r2_std"]
            correlations.reset_index(drop=True, inplace=True)

        correlations.to_feather(
            f"all_data/xwas/univariate_correlations/correlations/categories/correlations_{category}.feather"
        )
        upload_file(
            f"all_data/xwas/univariate_correlations/correlations/categories/correlations_{category}.feather",
            f"xwas/univariate_correlations/correlations/categories/correlations_{category}.feather",
        )
