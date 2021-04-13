import dash_bootstrap_components as dbc
import dash_html_components as html


def standard_card(id, name, color):
    return dbc.Col(
        dbc.Card(
            dbc.Button(name, id=id, color=color),
            color=color,
            inverse=True,
        )
    )


def faded_card(id, text, is_in=False):
    return dbc.Col(
        dbc.Fade(
            dbc.Card(html.P(text, className="card-text")),
            id=id,
            is_in=is_in,
            style={"transition": "opacity 100ms ease"},
        )
    )
