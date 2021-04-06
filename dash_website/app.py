import dash
import dash_bootstrap_components as dbc

# MODE = 'Heart'
MODE = "All"
APP = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], assets_url_path="/data", assets_folder="data")

APP.config.suppress_callback_exceptions = True
