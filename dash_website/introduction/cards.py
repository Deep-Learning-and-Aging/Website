import dash_bootstrap_components as dbc


def standard_card(id, name, color):
    return dbc.Col(
        dbc.Card(
            dbc.Button(name, id=id, color=color),
            color=color,
            inverse=True,
        )
    )