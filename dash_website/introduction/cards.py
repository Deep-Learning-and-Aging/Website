import dash_bootstrap_components as dbc


def standard_card(id, name):
    return dbc.Col(dbc.Button(name, id=id, color="Transparent", block=True))
