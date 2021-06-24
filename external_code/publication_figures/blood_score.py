import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website import DOWNLOAD_CONFIG, ALGORITHMS_RENDERING
from dash_website.age_prediction_performances import SCORES


if __name__ == "__main__":
    metric = "rmse"
    scores = load_feather(f"age_prediction_performances/scores_all_samples_per_participant.feather").set_index(
        ["dimension", "subdimension", "sub_subdimension"]
    )

    scores = scores.loc[
        [
            ("BloodCells", "BloodCount", "Scalars"),
            ("Biochemistry", "Blood", "Scalars"),
            ("Biochemistry", "Urine", "Scalars"),
        ]
    ]

    import plotly.graph_objs as go

    sorted_dimensions = scores.index.drop_duplicates()

    x_positions = pd.DataFrame(
        np.arange(5, 10 * len(sorted_dimensions) + 5, 10), index=sorted_dimensions, columns=["x_position"]
    )

    fig = go.Figure()
    fig.update_layout(
        xaxis={
            "tickvals": np.arange(5, 10 * len(sorted_dimensions) + 5, 10),
            "ticktext": ["Blood Cells", "Blood Biochemistry", "Urine Biochemistry"],
        }
    )

    algorithms = scores["algorithm"].drop_duplicates()

    hovertemplate = (
        "%{x}, score: %{y:.3f} +- %{customdata[0]:.3f}, sample size: %{customdata[1]} <extra>%{customdata[2]}</extra>"
    )

    min_score = min(scores[metric].min(), 0)

    for algorithm in algorithms:
        scores_algorithm = scores[scores["algorithm"] == algorithm]
        x_positions.loc[scores_algorithm.index]

        customdata = np.dstack(
            (
                scores_algorithm[f"{metric}_std"].values.flatten(),
                scores_algorithm["sample_size"].values.flatten(),
                [algorithm] * len(scores_algorithm.index),
            )
        )[0]
        fig.add_bar(
            x=x_positions.loc[scores_algorithm.index].values.flatten(),
            y=scores_algorithm[metric],
            error_y={"array": scores_algorithm[f"{metric}_std"], "type": "data"},
            name=ALGORITHMS_RENDERING[algorithm],
            hovertemplate=hovertemplate,
            customdata=customdata,
        )

    fig.update_layout(
        yaxis={
            "title": SCORES[metric],
            "showgrid": False,
            "zeroline": False,
            "title_font": {"size": 45},
            "dtick": 1 if metric == "rmse" else 0.1,
            "tickfont_size": 20,
        },
        xaxis={"showgrid": False, "zeroline": False, "tickfont": {"size": 30}},
        # height=800,
        # width=1000,
        margin={"l": 0, "r": 0, "b": 0, "t": 0},
        legend={"orientation": "h", "y": -0.1, "font": {"size": 30}},
    )

    print(f"Average {SCORES[metric]} = {scores[metric].mean().round(3)} +- {scores[metric].std().round(3)}")

    fig.show(config=DOWNLOAD_CONFIG)
