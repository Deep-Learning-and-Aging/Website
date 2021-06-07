import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def get_options(list_):
    list_label_value = []
    for value in list_:
        list_label_value.append({"value": value, "label": value})
    return list_label_value


def get_options_from_dict(dict_):
    list_label_value = []
    for key_value, label in dict_.items():
        d = {"value": key_value, "label": label}
        list_label_value.append(d)
    return list_label_value


def get_item_radio_items(id, items, legend, from_dict=True, value_idx=0):
    if from_dict:
        control = dbc.FormGroup(
            [
                html.P(legend),
                dcc.RadioItems(
                    id=id,
                    options=get_options_from_dict(items),
                    value=list(items.keys())[value_idx],
                    labelStyle={"display": "inline-block", "margin": "5px"},
                ),
                html.Br(),
            ]
        )
    else:
        control = dbc.FormGroup(
            [
                html.P(legend),
                dcc.RadioItems(
                    id=id,
                    options=get_options(items),
                    value=items[0],
                    labelStyle={"display": "inline-block", "margin": "5px"},
                ),
                html.Br(),
            ]
        )

    return control


def get_drop_down(id, items, legend, from_dict=True, value=None):
    if from_dict:
        if value is None:
            value = list(items.keys())[0]
        control = dbc.FormGroup(
            [
                html.P(legend),
                dcc.Dropdown(id=id, options=get_options_from_dict(items), value=value, clearable=False),
                html.Br(),
            ]
        )
    else:
        if value is None:
            value = items[0]
        control = dbc.FormGroup(
            [
                html.P(legend),
                dcc.Dropdown(id=id, options=get_options(items), value=value, clearable=False),
                html.Br(),
            ]
        )
    return control


def get_range_slider(id, min, max, legend):
    return dbc.FormGroup(
        [
            html.P(legend),
            dcc.RangeSlider(
                id=id,
                min=min,
                max=max,
                value=[min, max],
                marks=dict(zip(range(min, max + 1, 5), [str(elem) for elem in range(min, max + 1, 5)])),
                step=None,
            ),
            html.Br(),
        ]
    )


def get_check_list(id, items, legend):
    return dbc.FormGroup(
        [
            html.P(legend),
            dcc.Checklist(id=id, options=get_options(items), value=items, labelStyle={"display": "inline-block"}),
            html.Br(),
        ]
    )
