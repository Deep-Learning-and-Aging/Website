import dash
import dash_bootstrap_components as dbc
#MODE = 'Heart'
MODE = 'All'
filename = '/Users/samuel/Desktop/dash_app/data_final/'
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
app.config.suppress_callback_exceptions = True
server = app.server
