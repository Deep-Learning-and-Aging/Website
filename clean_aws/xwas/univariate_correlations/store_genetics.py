from dash_website.utils.aws_loader import load_csv


if __name__ == "__main__":
    genetics_table = load_csv("page17_GWASCorrelations/GWAS_correlations_Age.csv", index_col=0)

    genetics = genetics_table.stack(dropna=False).rename(
        index={
            "*": "set",
            "*instances01": "set_instances01",
            "*instances1.5x": "set_instances1.5x",
            "*instances23": "set_instances23",
        }
    )
    genetics.index.names = ["dimension_1", "dimension_2"]
    genetics.name = "correlation"

    genetics.reset_index().to_feather("data/xwas/univariate_correlations/genetics.feather")