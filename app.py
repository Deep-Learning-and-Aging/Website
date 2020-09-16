import dash
import dash_bootstrap_components as dbc
#MODE = 'Heart'
MODE = 'All'
filename = '/Users/samuel/Desktop/dash_app/assets2/'
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], assets_url_path = '/assets2', assets_folder = 'assets2')
app.config.suppress_callback_exceptions = True
