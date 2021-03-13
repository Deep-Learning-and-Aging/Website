## Instructions in order to use / modify the website.

Start by creating a path to your AWS credentials. You can edit the path in the file tools.py
Install the requirements : 
pip3 install -r requirements.txt when you are at the root of the directory.

In order to test the website locally, you can launch a server : 
python3 main.py
And access the website to this adress (default port 8050): 
http://localhost:8050/

## Structure of the website 
The website is constructed as follows : 
The index pointing to every subpage is the file main.py
Some tools are placed in the folder tools.py (useful to load data from AWS)
The content of each page (eg page1) are located in the page{pagenumber}.py (eg page1.py)


## Structure of a page 
The content of each page is always the same : 
Each page has a layout python object, and some attributes of this layout can be modified using callbacks.

## Example callback
For instance in the page 1 : 
We have this reset callback : 

@app.callback([Output("select_group_biomarkers", "value"),
               Output("select_view_biomarkers", "value"),
               Output("select_transformation_biomarkers", "value"),
               Output("select_biomarkers_of_group", "value"),
               Output("Ethnicity filter", "value")],
               [Input("reset_page1", "n_clicks")])
def reset(n):
    if n :
        if n > 0 :
            return [None, None, None, None, None]
    else :
        raise PreventUpdate()
        
For any input "reset_page1" (attribute of the layout) if the property "n_clicks" has been modified (user clicking on one button), it triggers the function reset 
which takes as an input the value of the attribute "n_clicks" (number of clicks).
It then associates some new values for the attribute "value" of the outputs :
- "select_group_biomarkers"
- "select_view_biomarkers" 
- "select_transformation_biomarkers"
- "select_biomarkers_of_group"

## How to deploy 
You need to have access to the GCP account and then create your own gcloud project :

gcloud init
you can deploy using :

gcloud app deploy
