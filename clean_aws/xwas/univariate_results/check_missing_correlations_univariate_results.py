from dash_website.utils.aws_loader import list_dir
import pandas as pd
from tqdm import tqdm

from dash_website import DIMENSIONS, ALL_CATEGORIES


def check_missing_correlations():
    list_objects = list_dir("page5_LinearXWASResults/LinearOutput/")

    list_indexes = []
    for category in ALL_CATEGORIES:
        for dimension in DIMENSIONS:
            list_indexes.append([category, dimension])

    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["category", "dimension"])
    correlations = pd.Series(False, index=indexes, name="Exists")

    for object_ in tqdm(list_objects):
        category_dimension = object_.split("/")[-1][20:-4]  # [: -4] for ., c, s, v
        if "set" in category_dimension:
            dimension = "set" + category_dimension.split("set")[-1]
            category = category_dimension[: -(len(dimension) + 1)]  # +1 for _
        else:
            dimension = category_dimension.split("_")[-1]
            category = category_dimension[: -(len(dimension) + 1)]  # +1 for _

        correlations[(category, dimension)] = True

    if (~correlations).sum() == 0:
        print("\n\n Every file is in AWS S3 for Linear XWAS Results ! \n\n")
    else:
        correlations[correlations == False].to_excel("missing_in_aws.xlsx")
