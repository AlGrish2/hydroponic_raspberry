import os
import requests
import base64

import logging
import boto3
from botocore.exceptions import ClientError


def read_file_as_bytes(file_path: str):
    with open(file_path, "rb") as image_file:
        file_bytes = image_file.read()
    return file_bytes


def _format_url(bucket_name: str, file_name: str) -> str:
    file_link = f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{file_name}"
    return file_link

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(
            file_name, 
            bucket, 
            object_name
            )
    except ClientError as e:
        logging.error(e)
        return False
    return _format_url(bucket, object_name)


if __name__ == "__main__":
    from config import videos_bucket
    
    print("Upload file to s3")
    file_path = "files/20220729_141520.mp4"
    print(videos_bucket)
    upload_file(file_path, videos_bucket)
    print("File uploaded to s3")