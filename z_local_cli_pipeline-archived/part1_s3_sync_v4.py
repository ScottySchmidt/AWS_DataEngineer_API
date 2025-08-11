# This version (v4) does not hardcode the series IDs.
import os
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import json
from hashlib import md5

# === CONFIGURATION ===
BLS_API_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"
BLS_API_KEY = "bd42a630a5f34afba1a0dbf6658f524a"
LOCAL_DIR = "bls_data_v4"
BUCKET_NAME = "rearc-bls-scott-2025"
AWS_PROFILE = "rearc-quest"

# Create local directory if missing
if not os.path.exists(LOCAL_DIR):
    os.makedirs(LOCAL_DIR)

# === AWS S3 CLIENT ===
session = boto3.Session(profile_name=AWS_PROFILE)
s3 = session.client("s3")

# === GET SERIES IDS DYNAMICALLY ===
def get_series_ids():
    url = "https://download.bls.gov/pub/time.series/pr/pr.series"
    response = requests.get(url)
    response.raise_for_status()
    lines = response.text.splitlines()
    # Skip header, take first column = series ID
    series_ids = [line.split()[0] for line in lines[1:]]
    return series_ids

# === FETCH DATA FROM BLS ===
def fetch_bls_data(series_ids, start_year="2020", end_year="2023"):
    headers = {"Content-type": "application/json"}
    data = json.dumps({
        "registrationKey": BLS_API_KEY,
        "seriesid": series_ids,
        "startyear": start_year,
        "endyear": end_year
    })
    response = requests.post(BLS_API_URL, data=data, headers=headers)
    response.raise_for_status()
    result = response.json()
    if result.get("status") == "REQUEST_SUCCEEDED":
        return result
    else:
        raise Exception(f"BLS API Request failed: {result}")

# === SAVE LOCALLY ===
def save_local(filename, data):
    filepath = os.path.join(LOCAL_DIR, filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    return filepath

# === HASH FILES ===
def file_md5(file_path):
    with open(file_path, "rb") as f:
        return md5(f.read()).hexdigest()

# === UPLOAD IF CHANGED ===
def upload_to_s3(local_file, bucket, key):
    try:
        head = s3.head_object(Bucket=bucket, Key=key)
        local_hash = file_md5(local_file)
        remote_hash = head['ETag'].strip('"')
        if local_hash == remote_hash:
            print(f"⏩ Skipped {local_file}, no changes detected.")
            return
    except ClientError:
        pass
    s3.upload_file(local_file, bucket, key)
    print(f"⬆️ Uploaded {local_file} to s3://{bucket}/{key}")

# === DELETE OLD FILES ===
def sync_delete_extra_files(bucket, valid_keys):
    s3_objects = s3.list_objects_v2(Bucket=bucket)
    if "Contents" in s3_objects:
        for obj in s3_objects["Contents"]:
            if obj["Key"] not in valid_keys:
                s3.delete_object(Bucket=bucket, Key=obj["Key"])
                print(f"🗑️ Deleted outdated file {obj['Key']} from S3")

# === MAIN ===
if __name__ == "__main__":
    try:
        print("Fetching list of series IDs...")
        series_ids = get_series_ids()

        print(f"Found {len(series_ids)} series to process.")
        bls_data = fetch_bls_data(series_ids, start_year="2020", end_year="2023")

        uploaded_keys = []
        for series in bls_data["Results"]["series"]:
            filename = f"{series['seriesID']}.json"
            local_file = save_local(filename, series)
            upload_to_s3(local_file, BUCKET_NAME, filename)
            uploaded_keys.append(filename)

        sync_delete_extra_files(BUCKET_NAME, uploaded_keys)
        print("✅ Full sync complete!")

    except Exception as e:
        print(f"Error: {e}")
