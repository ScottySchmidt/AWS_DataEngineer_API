"""
Part 2 — AWS Lambda: DataUSA → S3
Trigger: Amazon EventBridge (runs the 1st of each month), plus manual invoke for ad-hoc runs.

AWS Lambda that fetches DataUSA Population (Nation × Year) JSON and uploads it to S3.
Uses Python's stdlib urllib (no extra deps in Lambda) and writes to a fixed key, returning 200 on success or 500 on failures.

Why urllib?
- Lambda’s Python runtime doesn’t ship with `requests`.
- `urllib` is built-in, so no extra layer/package.
- If I need fancier HTTP later, I’ll add a `requests` layer.
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
    except Exception:
        return {"statusCode": 500, "body": "API fetch failed"}
    # Overwrite the "latest" snapshot
    key = "datausa_population.json" 
    #key = f"datausa_population_{datetime.now().strftime('%Y%m%d%H%M%S')}.json" #Timestamp version, but is harder to overrite later

    try:
        # Send file into S3 as JSON file:
        s3.put_object(Bucket=bucket, Key=key, Body=json.dumps(response_json))
    except Exception as e:
        # Failed:
        return {"statusCode": 500, "body": "S3 upload failed"}
    return {"statusCode": 200, "body": "upload complete"}
