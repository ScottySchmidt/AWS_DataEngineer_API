# Four-Part AWS Data Engineering Pipeline
This repository contains a complete four-stage pipeline demonstrating AWS-based data ingestion, storage, querying, and infrastructure automation. It showcases how to **deploy API-driven pipelines with GitHub CI/CD** using AWS services like **S3, Glue, RDS, IAM, Athena, and Lambda**. The project replicates real-world data engineering workflows from raw data ingestion to automated deployments — all built for scalability, maintainability, and automation.

1. **BLS Data to S3**  
   Fetches BLS productivity and inflation data using both the BLS Public API and direct file downloads with a custom `User-Agent`.  
   Compares file hashes to avoid re-uploading unchanged files, and stores results in Amazon S3.  
   [View Notebook](s3-pipeline-bls-api-part1.ipynb)

2. **API Request via AWS Lambda → S3**

   This step automates pulling BLS data via their API and dropping the JSON into S3 on demand (or on a schedule). It’s the    ingestion bridge between Part 1 (static BLS files) and Part 3 (query/analysis).
   
   [View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/lambda_bls_api_part2.py)
   
   **Output:** `s3://<your-bucket>/bls_data.json` (or a timestamped variant)

4. **Data Processing and Analysis**  
   Loads the stored data from S3 into Pandas for cleaning, transformation, and analytical reporting.  
   [View Notebook](aws-data-pipeline-warehouse-part3.ipynb)

5. **Automated Data Pipeline (Infrastructure as Code)**
   This stage packages the entire pipeline into a repeatable, deployable AWS infrastructure setup.  
   We’re using the AWS Cloud Development Kit (CDK) to define resources in Python and deploy them via CloudFormation.

   **Current Progress**
   - Created a Lambda function for data ingestion (BLS API and DataUSA API).
   - Added S3 buckets to store raw and processed datasets.
   - Defined environment variables in Lambda for bucket names and API keys.
   - Successfully deployed initial stack with AWS CDK.
   - Verified Lambda can be invoked and logs are streamed to CloudWatch.

---
More details will be added once all parts are completed and documented.
