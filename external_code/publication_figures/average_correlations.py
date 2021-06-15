import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website import MAIN_CATEGORIES_TO_CATEGORIES, DOWNLOAD_CONFIG


DIMENSIONS = ["Musculoskeletal"]

PAIRS_SUBDIMENSIONS = [
    ["MusculoskeletalScalars", "MusculoskeletalFullBody"],
    ["MusculoskeletalScalars", "MusculoskeletalSpine"],
    ["MusculoskeletalScalars", "MusculoskeletalHips"],
    ["MusculoskeletalScalars", "MusculoskeletalKnees"],
    ["MusculoskeletalFullBody", "MusculoskeletalSpine"],
    ["MusculoskeletalFullBody", "MusculoskeletalHips"],
    ["MusculoskeletalFullBody", "MusculoskeletalKnees"],
    ["MusculoskeletalSpine", "MusculoskeletalHips"],
    ["MusculoskeletalSpine", "MusculoskeletalKnees"],
    ["MusculoskeletalHips", "MusculoskeletalKnees"],
]

FULL_CATEGORY = (
    MAIN_CATEGORIES_TO_CATEGORIES["All"]
    + ["Phenotypic", "Genetics"]
    + [f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()]
)


def get_average_correlations():
    correlations_raw = load_feather(f"xwas/univariate_correlations/correlations.feather").set_index(
        ["dimension_1", "subdimension_1", "dimension_2", "subdimension_2", "category"]
    )
    correlations_raw.columns = pd.MultiIndex.from_tuples(
        list(map(eval, correlations_raw.columns.tolist())), names=["subset_method", "correlation_type"]
    )
    correlations_raw.reset_index(inplace=True)
    for index_dimension in [1, 2]:
        correlations_raw[f"squeezed_dimension_{index_dimension}"] = correlations_raw[
            f"dimension_{index_dimension}"
        ] + correlations_raw[f"subdimension_{index_dimension}"].replace("*", "")
    correlations_raw = correlations_raw.drop(
        columns=["dimension_1", "subdimension_1", "dimension_2", "subdimension_2"]
    ).set_index(["category", "squeezed_dimension_1", "squeezed_dimension_2"])

    list_indexes = []
    for dimension in ["Musculoskeletal"]:
        for category in FULL_CATEGORY:
            list_indexes.append([dimension, category])
    indexes = pd.MultiIndex.from_tuples(list_indexes, names=["dimension", "category"])

    list_columns = []
    for subset_method in ["union"]:
        for correlation_type in ["pearson"]:
            for observation in ["mean", "std"]:
                list_columns.append([subset_method, correlation_type, observation])
    columns = pd.MultiIndex.from_tuples(list_columns, names=["subset_method", "correlation_type", "observation"])

    averages_correlations = pd.DataFrame(None, index=indexes, columns=columns)

    for category in FULL_CATEGORY:
        correlations_category = correlations_raw.loc[category, ("union", "pearson")]

        averages_correlations.loc[
            ("Musculoskeletal", category), ("union", "pearson", "mean")
        ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].mean()
        averages_correlations.loc[
            ("Musculoskeletal", category), ("union", "pearson", "std")
        ] = correlations_category.loc[PAIRS_SUBDIMENSIONS].std()

    averages_correlations.columns = map(str, averages_correlations.columns.tolist())
    return averages_correlations.reset_index()


def get_graph_average(dimension_1, data_averages):
    import plotly.graph_objs as go

    averages = pd.DataFrame(data_averages).set_index(["dimension", "category"])
    averages.columns = pd.MultiIndex.from_tuples(
        list(map(eval, averages.columns.tolist())), names=["subset_method", "correlation_type", "observation"]
    )

    sorted_averages = averages.loc[
        (
            dimension_1,
            MAIN_CATEGORIES_TO_CATEGORIES["All"]
            + [f"All_{main_category}" for main_category in MAIN_CATEGORIES_TO_CATEGORIES.keys()],
        ),
        ("union", "pearson"),
    ].sort_values(by=["mean"], ascending=False)

    list_main_category = []
    list_categories = []
    # Get the ranking of subcategories per main category
    for main_category_group in MAIN_CATEGORIES_TO_CATEGORIES.keys():
        if main_category_group == "All":
            continue
        sorted_categories = (
            sorted_averages.swaplevel()
            .loc[MAIN_CATEGORIES_TO_CATEGORIES[main_category_group] + [f"All_{main_category_group}"]]
            .sort_values(by=["mean"], ascending=False)
        )
        print(
            "main_category",
            main_category_group,
            sorted_categories["mean"].mean().round(3),
            "+-",
            sorted_categories["mean"].std().round(3),
        )
        sorted_index_categories = sorted_categories.index.get_level_values("category")

        list_categories.extend(sorted_index_categories)
        list_main_category.extend([main_category_group] * len(sorted_index_categories))

    bars = go.Bar(
        x=[list_main_category + ["", "", ""], list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
        y=sorted_averages["mean"].swaplevel()[list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
        error_y={
            "array": sorted_averages["std"].swaplevel()[list_categories + ["FamilyHistory", "Genetics", "Phenotypic"]],
            "type": "data",
        },
        name="Correlations",
        marker_color="indianred",
    )

    title = f"Average average correlation across aging dimensions and X categories = {sorted_averages['mean'].mean().round(3)} +- {sorted_averages['mean'].std().round(3)}"
    y_label = "Average correlation"

    fig = go.Figure(bars)

    fig.update_layout(
        {
            "width": 2000,
            "height": 700,
            "xaxis": {"title": "X subcategory", "tickangle": 90, "showgrid": False, "title_font": {"size": 25}},
            "yaxis": {"title": y_label, "title_font": {"size": 25}},
            "margin": {"l": 0, "r": 0, "b": 0, "t": 0},
        }
    )

    print(title)
    return fig


if __name__ == "__main__":
    average_correlations = get_average_correlations()
    fig_average_correlations = get_graph_average("Musculoskeletal", average_correlations)

    fig_average_correlations.show(config=DOWNLOAD_CONFIG)
