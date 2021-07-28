import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html


def get_options_from_list(list_):
    list_label_value = []
    for value in list_:
        list_label_value.append({"value": value, "label": value})
    return list_label_value


def get_options_from_dict(dict_):
    list_label_value = []
    for key_value, label in dict_.items():
        list_label_value.append({"value": key_value, "label": label})
    return list_label_value


def get_item_radio_items(id, items, legend, from_dict=True, value_idx=0):
    if from_dict:
        options = get_options_from_dict(items)
    else:
        options = get_options_from_list(items)

    return dbc.FormGroup(
        [
            html.P(legend),
            dcc.RadioItems(
                id=id,
                options=options,
                value=options[value_idx]["value"],
                labelStyle={"display": "inline-block", "margin": "5px"},
            ),
        ]
    )


def get_drop_down(id, items, legend, from_dict=True, value=None, multi=False, clearable=False):
    if from_dict:
        options = get_options_from_dict(items)
    else:
        options = get_options_from_list(items)

    if value is None:
        value = options[0]["value"]

    if multi and type(value) != list:
        value = [value]

    return dbc.FormGroup(
        [
            html.P(legend),
            dcc.Dropdown(
                id=id,
                options=options,
                value=value,
                clearable=clearable,
                multi=multi,
                placeholder="Nothing is selected.",
            ),
        ]
    )


def get_check_list(id, items, legend, from_dict=True, value=None):
    if from_dict:
        options = get_options_from_dict(items)
    else:
        options = get_options_from_list(items)

    if value is None:
        value = options[0]["value"]

    return dbc.FormGroup(
        [
            html.P(legend),
            dcc.Checklist(id=id, options=options, value=[value], labelStyle={"display": "inline-block"}),
        ]
    )


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
