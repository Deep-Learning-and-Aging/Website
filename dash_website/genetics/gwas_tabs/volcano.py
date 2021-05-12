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
from dash_website import DOWNLOAD_CONFIG
from dash_website.genetics import DIMENSIONS_GWAS_VOLCANO, VOLCANO_TABLE_COLUMNS


def get_volcano():
    return dbc.Container(
        [
            dcc.Loading(dcc.Store(id="memory_volcano_gwas", data=get_data())),
            html.H1("Genetics - GWAS"),
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
                        [
                            dash_table.DataTable(
                                id="table_volcano_gwas",
                                columns=[{"name": i, "id": i} for i in list(VOLCANO_TABLE_COLUMNS.values())],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ],
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_data():
    return load_feather(f"genetics/gwas/size_effects.feather").to_dict()


def get_controls_volcano_gwas():
    return dbc.Card(
        get_drop_down(
            "dimension_volcano_gwas", ["All"] + DIMENSIONS_GWAS_VOLCANO, "Select a dimension:", from_dict=False
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
        customdata = size_effects.loc[
            [chromosome], ["SNP", "dimension", "p_value", "Gene", "Gene_type", "chromosome"]
        ].values

        fig.add_scatter(
            x=size_effects.loc[[chromosome], "size_effect"],
            y=-np.log(size_effects.loc[[chromosome], "p_value"] + +1e-323),
            mode="markers",
            name=f"Chromosome {chromosome}",
            customdata=customdata,
            hovertemplate=hovertemplate,
            marker={"size": size},
        )

    fig.update_layout(xaxis={"title": "Size Effect (SE)"}, yaxis={"title": "-log(p-value)"}, height=800)

    return fig
