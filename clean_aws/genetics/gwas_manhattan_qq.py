from dash_website.utils.aws_loader import copy_file, does_key_exists

PLOT_TYPE = {"manhattan": "GWAS_ManhattanPlot", "qq": "GWAS_QQPlot"}
DIMENSIONS = [
    "*instances1.5x",
    "*instances23",
    "Abdomen",
    "AbdomenLiver",
    "AbdomenPancreas",
    "All",
    "Arterial",
    "ArterialCarotids",
    "ArterialPulseWaveAnalysis",
    "Biochemistry",
    "BiochemistryBlood",
    "BiochemistryUrine",
    "Brain",
    "BrainCognitive",
    "BrainMRI",
    "Eyes",
    "EyesFundus",
    "EyesOCT",
    "Hearing",
    "Heart",
    "HeartECG",
    "HeartMRI",
    "ImmuneSystem",
    "Lungs",
    "Musculoskeletal",
    "MusculoskeletalFullBody",
    "MusculoskeletalHips",
    "MusculoskeletalKnees",
    "MusculoskeletalScalars",
    "MusculoskeletalSpine",
    "PhysicalActivity",
]

DIMENSIONS_TO_REPLACE = {
    "*instances1.5x": "set_instances1.5x",
    "*instances23": "set_instances23",
    "ImmuneSystem": "BloodCells",
}


if __name__ == "__main__":
    for plot_type in ["manhattan", "qq"]:
        for dimension in DIMENSIONS:
            copy_file(
                f"page10_GWASResults/Manhattan/{PLOT_TYPE[plot_type]}_Age_{dimension}.png",
                f"genetics/gwas/{plot_type}/{DIMENSIONS_TO_REPLACE.get(dimension, dimension)}.png",
            )
