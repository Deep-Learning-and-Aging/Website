from dash_website.utils.aws_loader import load_csv, upload_file


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

    squeezed_dimensions.to_feather("all_data/xwas/squeezed_dimensions_participant_and_time_of_examination.feather")
    upload_file(
        "all_data/xwas/squeezed_dimensions_participant_and_time_of_examination.feather",
        "xwas/squeezed_dimensions_participant_and_time_of_examination.feather",
    )
