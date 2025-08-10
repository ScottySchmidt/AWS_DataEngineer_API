# Four-Part AWS Data Engineering Pipeline
This repo showcases a four-stage AWS data pipeline—ingest → store → analyze → deploy as code. It’s CI/CD-ready and uses AWS S3, Lambda, SQS, CloudWatch, and the AWS CDK. The project mirrors real-world flows—from raw data ingestion to automated infrastructure—for scalability, maintainability, and automation. Future extensions: Athena, Glue, and RDS.

1. **API BLS Data to AWS S3**  
   Fetches BLS productivity and inflation data using both the BLS Public API and direct file downloads with a custom `User-Agent`.  
   Compares file hashes to skip unchanged files, and stores results in Amazon S3.  
   [View Notebook](s3-pipeline-bls-api-part1.ipynb)

2. **API Request via AWS Lambda → S3**  
   Automates pulling BLS data via their API and dropping the JSON into S3 on demand or on a schedule.  
   Acts as the ingestion bridge between Part 1 (static BLS files) and Part 3 (query/analysis).  
   [View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/lambda_bls_api_part2.py)


3. **Data Processing and Analysis**  
   Pulls data from **S3** into AWS Lambda, where it’s cleaned, merged, and transformed using **Pandas** before producing summary reports.  
   Work is also in progress to hook the pipeline into **Amazon Athena**, so the same datasets can be queried directly with SQL for faster, serverless analysis.  
   [View Notebook](aws-data-pipeline-warehouse-part3.ipynb)

4. **Automated Data Pipeline (Infrastructure as Code)**  

   In this part, I set up the pipeline so it can be deployed automatically with code instead of clicking around in the AWS console.  
   I used the **AWS Cloud Development Kit (CDK)** to write the setup in Python, and then deployed it with **CloudFormation**.  
   [View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/iac-cloudshell-cdk-part4.ipynb)

- Built two Lambda functions: one for **data ingestion** (BLS API + DataUSA API) and one for **report generation**.
- Added S3 buckets to store both raw and processed datasets.
- Set environment variables in Lambda for bucket names, API keys, and API endpoints.
- Linked **S3 Event Notifications** to send messages to SQS when new data is uploaded.
- Set **SQS triggers** to automatically run the report Lambda.
- Deployed everything with **AWS CDK** in **CloudShell**.
- Used **CloudWatch Events** to run the ingestion Lambda daily, and checked the logs in **CloudWatch Logs** to make sure it worked.

---
## Tech Stack & Services

**Core AWS**
- Amazon S3 — store raw + processed BLS datasets
- AWS Lambda — ingest API data and write to S3
- Amazon SQS — event-driven processing for reports (Part 4)
- Amazon CloudWatch Events — scheduled Lambda runs
- AWS IAM — least-privilege roles for Lambda/S3/SQS
- AWS CDK — infrastructure as code (deploy Lambda/S3/SQS)
- AWS Glue Data Catalog — crawl/catalog datasets *(planned)*
- Amazon Athena — SQL on S3 via Glue catalog *(planned)*

**Security & Secrets**
- Kaggle Secrets — store AWS keys / BLS API key in notebooks
- AWS Secrets Manager — centralized secrets for prod *(planned)*

**Data & SDKs**
- Python 3.11, Pandas
- Boto3 (AWS Python SDK)

**External Data Sources**
- BLS Public API + bulk files
- DataUSA Population API
