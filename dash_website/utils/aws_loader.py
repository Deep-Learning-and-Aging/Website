from boto3 import client, resource
from botocore.client import Config

import os
from io import BytesIO
import base64
import pandas as pd
import numpy as np
from matplotlib.image import imread

import yaml


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
    return pd.read_csv(BytesIO(obj["Body"].read()), **kwargs)


def load_excel(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    return pd.read_excel(BytesIO(obj["Body"].read()), **kwargs)


def load_parquet(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    return pd.read_parquet(BytesIO(obj["Body"].read()), **kwargs)


def load_feather(key_in_bucket, **kwargs):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    return pd.read_feather(BytesIO(obj["Body"].read()), **kwargs)


def load_src_image(key_in_bucket):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    image = BytesIO(obj["Body"].read())
    encoded_image = base64.b64encode(image.read())
    return f"data:image/png;base64,{encoded_image.decode()}"


def load_npy(key_in_bucket):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    return np.load(BytesIO(obj["Body"].read()))


def load_jpg(key_in_bucket):
    obj = CLIENT.get_object(Bucket=AWS_BUCKET_NAME, Key=key_in_bucket)
    return imread(BytesIO(obj["Body"].read()), format="jpg")


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


def copy_file(source_key, target_key):
    RESOURCE.Object(AWS_BUCKET_NAME, target_key).copy({"Bucket": AWS_BUCKET_NAME, "Key": source_key})


def upload_file(source_file_path, target_key):
    RESOURCE.Object(AWS_BUCKET_NAME, target_key).upload_file(Filename=source_file_path)
