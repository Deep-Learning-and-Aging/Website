from setuptools import setup

setup(
    name="dash_website",
    version="0.1",
    description="Website that shows the results on multi-dimensionality of aging.",
    packages=["dash_website"],
    requires=["setuptools==57.0.0", "wheel==0.36.2"],
    install_requires=[
        "gunicorn==20.1.0",
        "dash_bootstrap_components==0.13.0",
        "dash_core_components==1.17.1",
        "dash_html_components==1.1.4",
        "dash-gif-component==1.1.0",
        "dash_table==4.12.0",
        "dash==1.21.0",
        "sklearn==0.0",
        "numpy==1.21.1",
        "scipy==1.7.1",
        "pandas==1.3.1",
        "plotly==5.1.0",
        "boto3==1.18.19",
        "matplotlib==3.4.2",
        "pyarrow==5.0.0",
    ],
    extras_require={
        "dev": ["tqdm", "openpyxl", "ipykernel", "nbformat", "black", "pyyaml"],
    },
    entry_points={"console_scripts": ["launch_local_website=dash_website.index:launch_local_website"]},
)
