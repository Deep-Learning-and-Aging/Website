from setuptools import setup, find_packages

setup(
    name="dash_website",
    version="0.1",
    description="Website that shows the results on multi-dimensionality of aging.",
    packages=find_packages(),
    install_requires=[
        "dash_bootstrap_components",
        "dash_core_components",
        "dash_html_components",
        "dash-gif-component",
        "dash_table",
        "dash",
        "sklearn",
        "numpy",
        "scipy",
        "pandas",
        "gunicorn",
        "plotly",
        "boto3",
        "matplotlib",
        "black",
    ],
    entry_points={
        "console_scripts": [
            "launch_local_website=main:launch_website",
        ]
    },
)