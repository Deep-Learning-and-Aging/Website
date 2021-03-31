import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def get_options(list_):
    list_label_value = []
    for elem in list_:
        d = {"value": elem, "label": elem}
        list_label_value.append(d)
    return list_label_value


def get_options_from_dict(dict_):
    list_label_value = []
    for key_value, label in dict_.items():
        d = {"value": key_value, "label": label}
        list_label_value.append(d)
    return list_label_value


def get_correlation_type_radio_items(id):
    return dbc.FormGroup(
        [
            dbc.Label("Select correlation type :"),
            dcc.RadioItems(
                id=id,
                options=get_options(["pearson", "spearman"]),
                value="pearson",
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
        ]
    )


def get_subset_method_radio_items(id):
    return dbc.FormGroup(
        [
            dbc.Label("Select subset method :"),
            dcc.RadioItems(
                id=id,
                options=get_options(["all", "union", "intersection"]),
                value="union",
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
        ]
    )


def get_main_category_radio_items(id, categories):
    return dbc.FormGroup(
        [
            html.P("Select X main category: "),
            dcc.RadioItems(
                id=id,
                options=get_options(categories),
                value=categories[0],
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
            html.Br(),
        ]
    )


def get_item_radio_items(id, items):
    return dbc.FormGroup(
        [
            html.P("Select : "),
            dcc.RadioItems(
                id=id,
                options=get_options_from_dict(items),
                value=list(items.keys())[0],
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
            html.Br(),
        ]
    )


def get_category_drop_down(id):
    return dbc.FormGroup(
        [
            html.P("Select X subcategory: "),
            dcc.Dropdown(id=id, options=[{"value": "All", "label": "All"}], value="All"),
            html.Br(),
        ]
    )


def get_dimension_drop_down(id, dimension, idx_dimension=""):
    return dbc.FormGroup(
        [
            html.P(f"Select an aging dimension {idx_dimension}: "),
            dcc.Dropdown(id=id, options=get_options(dimension), value=dimension[0]),
            html.Br(),
        ],
    )