import time
import pandas as pd

from dash_website.utils.aws_loader import load_excel, load_parquet, load_feather

if __name__ == "__main__":
    time_excel = 0
    for idx_load_excel in range(10):
        start_excel = time.time()
        load_excel("xwas/univariate_results/linear_correlations.xlsx")
        time_excel += time.time() - start_excel

    print("Load excel", time_excel)

    time_parquet = 0
    for idx_load_excel in range(10):
        start_parquet = time.time()
        load_parquet("xwas/univariate_results/linear_correlations.parquet")
        time_parquet += time.time() - start_parquet

    print("Load parquet", time_parquet)

    time_feather = 0
    for idx_load_feather in range(10):
        start_feather = time.time()
        corr = load_feather("xwas/univariate_results/linear_correlations.feather").set_index("index")
        corr.columns = pd.MultiIndex.from_tuples(
            list(map(eval, corr.columns.tolist())), names=["dimension", "category", "variable"]
        )
        time_feather += time.time() - start_feather

    print("Load feather", time_feather)