from dash_website.utils.aws_loader import load_csv


if __name__ == "__main__":
    phenotypic_table = load_csv(
        "page4_correlations/ResidualsCorrelations/ResidualsCorrelations_bestmodels_*_Age_test.csv", index_col=0
    )

    phenotypic = phenotypic_table.stack(dropna=False).rename(
        index={
            "*": "set",
            "*instances01": "set_instances01",
            "*instances1.5x": "set_instances1.5x",
            "*instances23": "set_instances23",
        }
    )
    phenotypic.index.names = ["dimension_1", "dimension_2"]
    phenotypic.name = "correlation"

    phenotypic.reset_index().to_feather("data/xwas/univariate_correlations/phenotypic.feather")