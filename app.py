import dash
import dash_bootstrap_components as dbc

# MODE = 'Heart'
MODE = "All"
app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], assets_url_path="/data", assets_folder="data")
app.config.suppress_callback_exceptions = True
