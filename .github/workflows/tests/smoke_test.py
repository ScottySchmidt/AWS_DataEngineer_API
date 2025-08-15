# tests/smoke_test.py
# Basic smoke test for AWS_DataEngineer_API

import os

def test_env_present():
    # Make sure CI loaded the secrets we expect
    for var in ("AWS_ACCESS_KEY_ID","AWS_SECRET_ACCESS_KEY","AWS_REGION","BUCKET_NAME","BLS_API_KEY"):
        assert os.getenv(var), f"Missing env var: {var}"

# Optional AWS ping (enable later by setting RUN_AWS_SMOKE=1 in the workflow env)
def test_optional_aws_s3_head():
    if os.getenv("RUN_AWS_SMOKE") != "1":
        import pytest; pytest.skip("Skipping AWS smoke (set RUN_AWS_SMOKE=1 to enable)")
    import boto3
    s3 = boto3.client("s3", region_name=os.getenv("AWS_REGION", "us-east-1"))
    s3.head_bucket(Bucket=os.environ["BUCKET_NAME"])

