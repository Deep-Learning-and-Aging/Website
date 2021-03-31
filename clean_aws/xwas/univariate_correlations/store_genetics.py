import pandas as pd

from dash_website.utils.aws_loader import load_csv
from dash_website import DIMENSIONS

if __name__ == "__main__":
    list_indexes = []
    for dimension_1 in DIMENSIONS:
        for dimension_2 in DIMENSIONS:
            list_indexes.append([dimension_1, dimension_2])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["dimension_1", "dimension_2"])
    genetics = pd.DataFrame(None, index=indexes, columns=["correlation"])

    genetics_table = load_csv("page17_GWASCorrelations/GWAS_correlations_Age.csv", index_col=0)

    genetics_raw = genetics_table.stack(dropna=False).rename(
        index={
            "*": "set",
            "*instances01": "set_instances01",
            "*instances1.5x": "set_instances1.5x",
            "*instances23": "set_instances23",
        }
    )
    genetics_raw.index.names = ["dimension_1", "dimension_2"]
    genetics_raw.name = "correlation"

    genetics["correlation"] = genetics_raw

    genetics.reset_index().to_feather("data/xwas/univariate_correlations/genetics.feather")