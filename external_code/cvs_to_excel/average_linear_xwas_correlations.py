import pandas as pd
import numpy as np

if __name__ == "__main__":
    for subset_method in ["All", "Union", "intersection"]:
        for correlation_type in ["Pearson", "Spearman"]:
            correlations = pd.read_csv(
                f"../../data/page6_LinearXWASCorrelations/average_correlations/Correlations_comparisons_{subset_method}_{correlation_type}.csv",
                index_col=[0],
            )
            correlations.index = pd.MultiIndex.from_tuples(
                correlations.index.str.split("_").tolist(), names=("organ_2", "organ_1")
            )

            correlations.to_excel(
                f"../../data/page6_LinearXWASCorrelations/average_correlations/Correlations_comparisons_{subset_method}_{correlation_type}.xlsx"
            )
