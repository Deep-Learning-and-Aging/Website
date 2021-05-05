import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import pandas as pd

from dash_website.app import APP
from dash_website.utils.controls import get_item_radio_items
from dash_website.utils.aws_loader import load_feather
from dash_website import DOWNLOAD_CONFIG, MAIN_CATEGORIES_TO_CATEGORIES, RENAME_DIMENSIONS
from dash_website.xwas.univariate_results_tabs import ITEMS_LEGEND, ITEMS_COLORSCALE, ITEMS_TITLES


def get_summary():
    return dbc.Container(
        [
            dcc.Loading([dcc.Store(id="memory_summary", data=get_data())]),
            html.H1("Univariate XWAS - Results"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col([get_controls_tab(), html.Br(), html.Br()], md=3),
                    dbc.Col([html.H2(id="title_summary"), dcc.Graph(id="graph_summary", config=DOWNLOAD_CONFIG)], md=9),
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather(f"xwas/univariate_results/summary.feather").to_dict()


def get_controls_tab():
    return dbc.Card(
        [
            get_item_radio_items(
                "main_category_summary",
                list(MAIN_CATEGORIES_TO_CATEGORIES.keys()),
                "Select X main category: ",
                from_dict=False,
            ),
            get_item_radio_items("item_summary", ITEMS_LEGEND, "Select :"),
        ]
    )


@APP.callback(
    [Output("graph_summary", "figure"), Output("title_summary", "children")],
    [Input("item_summary", "value"), Input("main_category_summary", "value"), Input("memory_summary", "data")],
)
def _fill_summary_heatmap(item, main_category, data):
    import plotly.graph_objects as go

    if main_category == "All":
        list_categories = [f"All_{main_category}"] + list(
            pd.Index(MAIN_CATEGORIES_TO_CATEGORIES[main_category]).drop(["Genetics", "Phenotypic"])
        )
    else:
        list_categories = [f"All_{main_category}"] + MAIN_CATEGORIES_TO_CATEGORIES[main_category]

    summary = pd.DataFrame(data).set_index(["dimension", "category"])
    summary.columns = pd.MultiIndex.from_tuples(
        list(map(eval, summary.columns.tolist())), names=["item", "observation"]
    )

    summary_item_percentage = (
        100
        * summary.reset_index().pivot(
            index=[("dimension", "")], columns=[("category", "")], values=(item, "percentage")
        )
    ).astype(int)
    summary_item_percentage_category = summary_item_percentage[list_categories].rename(index=RENAME_DIMENSIONS)
    summary_item_percentage_category.index.name = "dimension"
    summary_item_percentage_category.columns.name = "category"

    summary_item_number = summary.reset_index().pivot(
        index=[("dimension", "")], columns=[("category", "")], values=(item, "number")
    )
    summary_item_number_category = summary_item_number[list_categories].rename(index=RENAME_DIMENSIONS)
    summary_item_percentage_category.index.name = "dimension"
    summary_item_percentage_category.columns.name = "category"

    hovertemplate = "<br>".join(
        [
            "X main category: %{x}",
            "Aging dimension: %{y}",
            f"{ITEMS_LEGEND[item]}: " + "%{customdata} ~ %{z} % of the variables",
            "<extra></extra>",
        ]
    )

    heatmap = go.Heatmap(
        z=summary_item_percentage_category,
        x=summary_item_percentage_category.columns,
        y=summary_item_percentage_category.index,
        customdata=summary_item_number_category,
        hovertemplate=hovertemplate,
        colorscale=ITEMS_COLORSCALE[item],
        zmin=0,
        zmax=100,
    )

    fig = go.Figure(heatmap)
    fig.update_layout(
        {
            "xaxis": {"title": "X subcategory", "tickangle": 90},
            "yaxis": {"title": "Aging dimension"},
            "width": max(30 * summary_item_percentage_category.shape[1], 500),
            "height": 30 * summary_item_percentage_category.shape[0],
        }
    )

    return fig, ITEMS_TITLES[item]