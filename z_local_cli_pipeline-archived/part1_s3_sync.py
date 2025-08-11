import os
import time
import requests
import boto3
from botocore.exceptions import NoCredentialsError, ClientError
from hashlib import md5

# === CONFIGURATION ===
BLS_BASE_URL = "https://download.bls.gov/pub/time.series/pr/"
FILES = [
    "pr.class", "pr.contacts", "pr.data.0.Current", "pr.data.1.AllData",
    "pr.duration", "pr.footnote", "pr.measure", "pr.period",
    "pr.seasonal", "pr.sector", "pr.series", "pr.txt"
]
LOCAL_DIR = "bls_data"
BUCKET_NAME = "rearc-bls-scott-2025"
AWS_PROFILE = "rearc-quest"

# === HEADERS ===
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; RearcDataQuest/1.0; +mailto:scott.schmidt1989@yahoo.com)",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

# Use persistent session
session = requests.Session()
session.headers.clear()
session.headers.update(HEADERS)

print("DEBUG: Session headers being sent:", session.headers)

# Create local data directory
os.makedirs(LOCAL_DIR, exist_ok=True)

# Connect to AWS S3
session_boto = boto3.Session(profile_name=AWS_PROFILE)
s3 = session_boto.client("s3")

def md5sum(filename):
    with open(filename, "rb") as f:
        return md5(f.read()).hexdigest()

def download_file(filename):
    url = f"{BLS_BASE_URL}{filename}"
    local_path = os.path.join(LOCAL_DIR, filename)
    print(f"\nDEBUG: Attempting to download {url}")

    try:
        response = session.get(url, timeout=30)
        print(f"DEBUG: Response status for {filename}: {response.status_code}")
        print(f"DEBUG: Response headers: {response.headers}")
        if response.status_code == 200:
            with open(local_path, "wb") as f:
                f.write(response.content)
            print(f"Saved {filename} to {local_path} ({len(response.content)} bytes)")
            return local_path
        else:
            print(f"Failed to download {filename}. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"ERROR downloading {filename}: {e}")
        return None

def upload_to_s3(local_path, s3_key):
    try:
        print(f"DEBUG: Checking if {s3_key} exists in S3...")
        s3.head_object(Bucket=BUCKET_NAME, Key=s3_key)
        s3.download_file(BUCKET_NAME, s3_key, "tmp_s3_file")
        if md5sum(local_path) == md5sum("tmp_s3_file"):
            print(f"{s3_key} is up to date. Skipping upload.")
            os.remove("tmp_s3_file")
            return
        os.remove("tmp_s3_file")
    except ClientError as e:
        print(f"DEBUG: {s3_key} not found in S3 or access denied: {e}")

    try:
        print(f"DEBUG: Uploading {s3_key} to S3...")
        s3.upload_file(local_path, BUCKET_NAME, s3_key, ExtraArgs={'ACL': 'public-read'})
        print(f"Uploaded {s3_key} to S3 bucket {BUCKET_NAME}")
    except NoCredentialsError:
        print("ERROR: AWS credentials not available. Check your AWS CLI profile.")
    except Exception as e:
        print(f"ERROR uploading {s3_key} to S3: {e}")

if __name__ == "__main__":
    for file in FILES:
        local_file = download_file(file)
        if local_file:
            upload_to_s3(local_file, file)
        time.sleep(2)
