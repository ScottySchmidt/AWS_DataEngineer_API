# tests/smoke_test.py
# Basic smoke test for AWS_DataEngineer_API

import boto3

def test_boto3_version():
    print("Boto3 version:", boto3.__version__)
    assert boto3.__version__ is not None

if __name__ == "__main__":
    test_boto3_version()
    print("Smoke test passed")
