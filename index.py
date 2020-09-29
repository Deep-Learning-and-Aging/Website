import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from collections import OrderedDict
import sys
from app import app
from pages import menu, page1, page2, page3, page4, page5, page6, page7, page8, page9, page10, page11, page12, page13
num_pages = 13
top_bar = html.Div([
    dbc.Nav(
        [
            dbc.NavItem(dbc.NavLink("Menu", href="/", active=True, id="menu-link")),
            dbc.NavItem(dbc.NavLink("Biomarkers", href="/pages/page1", id="page1-link")),
            dbc.NavItem(dbc.NavLink("Age prediction performances", href="/pages/page2", id="page2-link")),
            dbc.DropdownMenu([dbc.DropdownMenuItem("Scalars", href="/pages/page3", id="page3-link"),
                              dbc.DropdownMenuItem("Images", href="/pages/page9", id="page9-link"),
                              dbc.DropdownMenuItem("Videos", href="/pages/page12", id="page12-link"),
                              dbc.DropdownMenuItem("TimeSeries", href="/pages/page13", id="page13-link")],
                              label="Features importances",
                              nav=True
                             ),
            #dbc.NavItem(dbc.NavLink("Features importances", href="/pages/page3", id="page3-link")),
            #dbc.NavItem(dbc.NavLink("Attention Maps", href="/pages/page9", id="page9-link")),
            dbc.DropdownMenu([dbc.DropdownMenuItem("GWAS - Results", href="/pages/page10", id="page10-link"),
                              dbc.DropdownMenuItem("GWAS - Heritability", href="/pages/page11", id="page11-link")],
                              label="GWAS",
                              nav=True
                             ),
            #dbc.NavItem(dbc.NavLink("GWAS", href="/pages/page10", id="page10-link")),
            dbc.DropdownMenu([dbc.DropdownMenuItem("Linear XWAS - Results", href="/pages/page5", id="page5-link"),
                              dbc.DropdownMenuItem("Linear XWAS - Correlations", href="/pages/page6", id="page6-link")],
                              label="Linear XWAS",
                              nav=True
                             ),
            dbc.DropdownMenu([dbc.DropdownMenuItem("Multivariate XWAS - Results", href="/pages/page7", id="page7-link"),
                              dbc.DropdownMenuItem("Multivariate XWAS - Correlations", href="/pages/page8", id="page8-link")],
                              label="Multivariate XWAS",
                              nav=True
                             ),
            dbc.NavItem(dbc.NavLink("Correlation between accelerated aging dimensions", href="/pages/page4", id="page4-link")),
        ],
    fill=True,
    pills=True),

],
style={
    "top": 0,
    "left": 50,
    "bottom": 0,
    "right":50,
    #"width": "80%",
    "padding": "1rem 1rem",
})

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    top_bar,
    html.Hr(),
    html.Div(id='page-content'),
    ],
style={"height": "100vh", 'fontSize': 10})


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if 'page' in pathname :
        num_page = int(pathname.split('/')[-1][4:])
        return getattr(globals()['page%s' % num_page], 'layout')
    elif pathname == '/':
        return menu.layout
    else:
        return '404'

@app.callback([Output('menu-link', 'active')] + [Output('page%s-link' % i, 'active') for i in range(1, num_pages + 1)],
              [Input('url', 'pathname')])
def _(pathname):
    map_path_name_id = OrderedDict()
    map_path_name_id['/'] = 'menu-link'
    for i in range(1, num_pages + 1):
        map_path_name_id['/pages/page%s' % i] = 'page%s-link' % i

    output = [False] * (1 + num_pages) # Menu + pages
    count = 0
    for path_, id_ in map_path_name_id.items():
        if path_ == pathname:
            output[count] = True
        count += 1
    #print(output)
    return output



if __name__ == '__main__':
    app.run_server(debug=True)
