import dash
import dash_html_components as html
import base64
from dash_website.utils.aws_loader import load_png

app = dash.Dash()
image_filename = "all_data/introduction/logo_hms.png"  # replace with your own image

local = open(image_filename, "rb")
aws = load_png("introduction/logo_hms.png")

encoded_image = base64.b64encode(aws.read())
app.layout = html.Div([html.Img(src="data:image/png;base64,{}".format(encoded_image.decode()))])

if __name__ == "__main__":
    app.run_server(debug=True)