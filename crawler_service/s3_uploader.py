import boto3
import json

s3 = boto3.client("s3")

BUCKET_NAME = "webknowledge-raw-datas"

def upload_to_s3(df):

    data = df.to_json()
    s3.put_object(
        Bucket = BUCKET_NAME,
        Key = "crawled/site_data.json",
        Body = data
    )

