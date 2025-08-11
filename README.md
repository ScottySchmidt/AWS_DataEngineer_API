# Four-Part AWS Data Engineering Pipeline
This repo showcases a four-stage AWS data pipeline—ingest → store → analyze → deploy as code. It’s **CI/CD-ready** and uses **Amazon S3, AWS Lambda, Amazon SQS, Amazon EventBridge (schedule), and the AWS CDK**. 
The project mirrors real-world flows—from raw ingestion to automated infrastructure—for scalability, maintainability, and automation. *Future extentions:* Amazon Athena, AWS Glue, and Amazon RDS.

1. **API BLS Data → AWS S3**  
   Fetches BLS productivity and inflation data using my registered public API and bulk files (with a compliant custom User-Agent).  
   Compares file hashes to skip unchanged files, and stores results in Amazon S3.  
   **[View Notebook](s3-pipeline-bls-api-part1.ipynb)**

2. **API Request via AWS Lambda → S3**  
   Automates pulling BLS API data and dropping JSON into S3 on a monthly schedule using Amazon EventBridge.
   Acts as a bridge between Part 1 and Part 3 data analysis.  
   **[View Script](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/lambda_bls_api_part2.py)**

   **Method Two:— Glue + Athena (Alternative)**  
   Query S3-hosted BLS data via:  
   - **AWS Glue Data Catalog** – automated dataset crawling for schema management  
   - **Amazon Athena** – serverless SQL queries directly on S3 data  
   **[View Notebook](glue-athena-part2-5a.ipynb)**

3. **Data Processing and Analysis**  
   Loads data from **S3** into a **Pandas notebook** (Kaggle) where it’s cleaned, merged, and transformed before producing summary reports.  
   Work is in progress to add **Amazon Athena** so the same datasets can be queried directly with SQL for faster, serverless analysis.  
   **[View Notebook](aws-data-pipeline-warehouse-part3.ipynb)**

4. **Automated Data Pipeline (Infrastructure as Code)**  
   Ship the stack with AWS CDK (Python) from CloudShell — no local setup.
   - Lambdas: ingest (BLS + DataUSA) and report (joins + summaries)
   - Storage: S3 with `raw/` → `processed/`
   - Events: EventBridge (daily) runs ingest; S3 `raw/` create → SQS → triggers report Lambda
   - SQS (why): buffer + retry so events don’t pile up or get lost — S3 drops a note, report picks it up
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/iac-cloudshell-cdk-part4.ipynb)**

   **Option B- Core AWS CDK with Python (Alternative)** 
    I used AWS CDK to spin up S3 + two Lambdas. CDK also makes the IAM roles for me. No SQS in this version.
    - When a new file lands in `raw/`, the report Lambda runs right away.
    - A schedule (EventBridge) runs the ingest Lambda on the 1st of each month.
    **[View Notebook (coming soon)](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/iac-cloudshell-cdk-part4.ipynb)**

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

### Security, SDKs & Data Sources
- **Secrets:** Kaggle Secrets (dev/demo); AWS Secrets Manager
- **SDKs:** Python 3.11, Pandas, Boto3 (AWS SDK for Python)
- **Sources:** BLS Public API + bulk files; DataUSA API
