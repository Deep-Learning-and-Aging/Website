from functools import lru_cache
import time
from dash_website.utils.aws_loader import load_feather


@lru_cache()
def load_data(dimension):
    return load_feather(f"xwas/univariate_results/linear_correlations_{dimension}.feather")


time_1 = time.time()
load_data("Abdomen")
print("Uncached results")
print(time.time() - time_1)

time_2 = time.time()
load_data("Abdomen")
print("Cached results")
print(time.time() - time_2)