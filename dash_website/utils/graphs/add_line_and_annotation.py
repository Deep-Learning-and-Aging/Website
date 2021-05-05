def add_line_and_annotation(
    text, first_axis, second_axis, min_position, max_position, inner_margin, outer_margin, textangle, size, final=False
):
    if not final:
        to_match_heatmap = -10 / 2
        position = min_position
    else:
        to_match_heatmap = +10 / 2
        position = max_position
    return (
        {
            "type": "line",
            "xref": "x",
            "yref": "y",
            f"{first_axis}0": float(position + to_match_heatmap),
            f"{second_axis}0": inner_margin,
            f"{first_axis}1": float(position + to_match_heatmap),
            f"{second_axis}1": outer_margin,
            "line": {"color": "Black", "width": 0.5},
        },
        {
            "text": text,
            "xref": "x",
            "yref": "y",
            first_axis: float((min_position + max_position) / 2),
            second_axis: (inner_margin + outer_margin) / 2,
            "showarrow": False,
            "textangle": textangle,
            "font": {"size": size},
        },
    )
