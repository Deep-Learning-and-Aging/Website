from boto3 import client, resource
from botocore.client import Config

import os
from io import BytesIO
import re
import base64
import pandas as pd
import yaml
from matplotlib.image import imread


if os.environ.get("AWS_ACCESS_KEY_ID") is None:
    with open("app.yaml", "r") as app_yaml:
        app_file = yaml.safe_load(app_yaml)
    os.environ["AWS_ACCESS_KEY_ID"] = app_file["env_variables"]["AWS_ACCESS_KEY_ID"]
    os.environ["AWS_SECRET_ACCESS_KEY"] = app_file["env_variables"]["AWS_SECRET_ACCESS_KEY"]

AWS_BUCKET_NAME = "age-prediction-site"
CLIENT = client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    config=Config(signature_version="s3v4"),
)
RESOURCE = resource(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
    config=Config(signature_version="s3v4"),
)


def load_csv(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    df = pd.read_csv(BytesIO(obj["Body"].read()), **kwargs)
    return df


def load_excel(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    df = pd.read_excel(BytesIO(obj["Body"].read()), **kwargs)
    return df


def load_parquet(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    df = pd.read_parquet(BytesIO(obj["Body"].read()), **kwargs)
    return df


def load_feather(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    df = pd.read_feather(BytesIO(obj["Body"].read()), **kwargs)
    return df


def load_src_image(key_in_bucket):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    image = BytesIO(obj["Body"].read())
    encoded_image = base64.b64encode(image.read())
    return f"data:image/png;base64,{encoded_image.decode()}"


def list_dir(path_dir):
    paginator = CLIENT.get_paginator("list_objects_v2")
    paginator_linear_xwas = paginator.paginate(Bucket=AWS_BUCKET_NAME, Prefix=path_dir)

    list_objects = []

    for partial_paginator in paginator_linear_xwas:
        for object in partial_paginator["Contents"]:
            list_objects.append(object["Key"])

    return list_objects


def does_key_exists(key):
    bucket = RESOURCE.Bucket(AWS_BUCKET_NAME)

    objects = list(bucket.objects.filter(Prefix=key))
    if any([w.key == key for w in objects]):
        return True
    else:
        return False
