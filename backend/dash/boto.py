import logging
import os
import time

import boto3

import backend.settings as settings

logger = logging.getLogger("app")


session = boto3.session.Session()
client = session.client(
    "s3",
    region_name=settings.AWS_S3_REGION_NAME,
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)


def push(body, filetype, tmp_loc):
    if not os.path.isfile(tmp_loc):
        return "we don't have the file"

    filename = os.path.split(body)[1]
    rand = str(time.time()).replace(".", "_")
    dest = f"{settings.AWS_S3_ROOT}/{filetype}/{rand}_{filename}"
    try:
        delete(filename)
    except Exception as e:
        logger.info(f"nothing to delete here >>{e}")
    content_type = "image/png"
    if dest.lower().endswith("pdf"):
        content_type = "application/pdf"
    elif dest.lower().endswith("png"):
        content_type = "image/png"
    else:
        content_type = "application/octet-stream"
    with open(tmp_loc, "rb") as f:
        client.put_object(
            Bucket=settings.AWS_STORAGE_BUCKET_NAME,
            Key=dest,
            Body=f,
            ContentType=content_type,
            ACL="public-read",
        )
    return f"{settings.AWS_CDN_URL}/{dest}"


def get(filename, target):
    logger.info(settings.AWS_STORAGE_BUCKET_NAME, filename, target)
    return client.download_file(settings.AWS_STORAGE_BUCKET_NAME, filename, target)


def delete(filename):
    client.delete_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key=filename)
