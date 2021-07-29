from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_drop_down
from dash_website import DIMENSIONS_SUBDIMENSIONS, DOWNLOAD_CONFIG
from dash_website.genetics import VOLCANO_TABLE_COLUMNS
from dash_website.genetics.gwas_tabs import DIMENSIONS_TO_DROP_VOLCANO


def get_volcano():
    return dbc.Container(
        [
            dcc.Loading(
                dcc.Store(id="memory_volcano_gwas", data=load_feather("genetics/gwas/size_effects.feather").to_dict())
            ),
            html.H1("Associations - GWAS"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            get_controls_volcano_gwas(),
                            html.Br(),
                            html.Br(),
                        ],
                        width={"size": 3},
                    ),
                    dbc.Col(
                        [
                            dcc.Loading(
                                [
                                    html.H2("Vocalno plot"),
                                    dcc.Graph(id="graph_volcano_gwas", config=DOWNLOAD_CONFIG),
                                ]
                            )
                        ],
                        width={"size": 6},
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Loading(
                            [
                                dash_table.DataTable(
                                    id="table_volcano_gwas",
                                    columns=[{"id": key, "name": name} for key, name in VOLCANO_TABLE_COLUMNS.items()],
                                    style_cell={"textAlign": "left"},
                                    sort_action="custom",
                                    sort_mode="single",
                                )
                            ]
                        ),
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_volcano_gwas():
    return dbc.Card(
        get_drop_down(
            "dimension_volcano_gwas",
            pd.Index(DIMENSIONS_SUBDIMENSIONS).drop(DIMENSIONS_TO_DROP_VOLCANO),
            "Select a dimension:",
            from_dict=False,
        )
    )


@APP.callback(
    Output("graph_volcano_gwas", "figure"),
    [
        Input("dimension_volcano_gwas", "value"),
        Input("memory_volcano_gwas", "data"),
    ],
)
def _fill_graph_volcano_gwas(dimension, data_volcano_gwas):
    import plotly.graph_objs as go

    size_effects = pd.DataFrame(data_volcano_gwas)

    if dimension != "All":
        size_effects = size_effects.set_index("dimension").loc[[dimension]].reset_index()
    size_effects.set_index("chromosome", drop=False, inplace=True)

    fig = go.Figure()

    hovertemplate = "SNP : %{customdata[0]}<br> Dimension : %{customdata[1]}<br> p-value : %{customdata[2]}<br> Gene : %{customdata[3]}<br> Gene Type : %{customdata[4]}<br><extra> Chromosome %{customdata[5]}</extra>"

    fig.add_scatter(
        x=[
            size_effects["size_effect"].min() - size_effects["size_effect"].std(),
            size_effects["size_effect"].max() + size_effects["size_effect"].std(),
        ],
        y=[-np.log(5e-8), -np.log(5e-8)],
        name="Significance level after FDR",
        mode="lines",
    )

    if dimension != "all":
        size = 5
    else:
        size = 3

    for chromosome in size_effects["chromosome"].drop_duplicates():
        customdata = size_effects.loc[[chromosome], ["SNP", "dimension", "p_value", "Gene", "Gene_type", "chromosome"]]
        customdata["p_value"] = customdata["p_value"].apply(lambda x: "%.3e" % x)

        fig.add_scatter(
            x=size_effects.loc[[chromosome], "size_effect"],
            y=-np.log(size_effects.loc[[chromosome], "p_value"] + +1e-323),
            mode="markers",
            name=f"Chromosome {chromosome}",
            customdata=customdata.values,
            hovertemplate=hovertemplate,
            marker={"size": size},
        )

    fig.update_layout(
        xaxis={"title": "Size Effect (SE)"},
        xaxis_title_font={"size": 25},
        yaxis={"title": "-log(p-value)"},
        yaxis_title_font={"size": 25},
        height=800,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
    )

    return fig


@APP.callback(
    Output("table_volcano_gwas", "data"),
    [
        Input("dimension_volcano_gwas", "value"),
        Input("memory_volcano_gwas", "data"),
        Input("table_volcano_gwas", "sort_by"),
    ],
)
def _sort_table(dimension, data_volcano_gwas, sort_by_col):
    size_effects = pd.DataFrame(data_volcano_gwas)

    if dimension != "All":
        size_effects = size_effects.set_index("dimension").loc[[dimension]].reset_index()

    if sort_by_col is not None and len(sort_by_col) > 0:
        is_ascending = sort_by_col[0]["direction"] == "asc"
        size_effects.sort_values(sort_by_col[0]["column_id"], ascending=is_ascending, inplace=True)
    else:
        size_effects.sort_values("p_value", inplace=True)

    size_effects["p_value"] = size_effects["p_value"].apply(lambda x: "%.3e" % x)
    size_effects[pd.Index(VOLCANO_TABLE_COLUMNS.keys()).drop("p_value")] = size_effects[
        pd.Index(VOLCANO_TABLE_COLUMNS.keys()).drop("p_value")
    ].round(3)

    return size_effects[VOLCANO_TABLE_COLUMNS].to_dict("records")
