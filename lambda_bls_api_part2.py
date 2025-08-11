"""
Ingest DataUSA population snapshot → AWS S3.

Why urllib?
- AWS Lambda's base Python runtime doesn't include the third-party 'requests' library.
- Using urllib.request (stdlib) avoids packaging a layer/dependency. It's lighter and just works.
- If we ever need advanced HTTP niceties, we can switch to 'requests' via a Lambda Layer.

Env:
- BUCKET_NAME: target S3 bucket
"""
import os, json, boto3
from datetime import datetime
import urllib.request
import os

s3 = boto3.client("s3", region_name="us-east-1")

def lambda_handler(event, context):
    bucket = os.environ.get("BUCKET_NAME")
    url = "https://honolulu-api.datausa.io/tesseract/data.jsonrecords?cube=acs_yg_total_population_1&drilldowns=Year%2CNation&locale=en&measures=Population"

    try:
        with urllib.request.urlopen(url) as response:
            data = response.read()
            response_json = json.loads(data)
    except Exception as e:
        return {"statusCode": 500, "body": f"API request failed: {e}"}
    key = "datausa_population.json"
    #key = f"datausa_population_{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
    try:
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(response_json))
    except Exception as e:
        return {"statusCode": 500, "body": f"S3 upload failed: {e}"}
    return {"statusCode": 200, "body": f"✅ Uploaded key to bucket"}
