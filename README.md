   # Four-Part AWS Data Engineering Pipeline
A four-stage pipeline on AWS — ingest → store → analyze → deploy-as-code.  
Uses S3, Lambda, SQS, EventBridge, Glue, Athena and CDK.  Deployed from AWS CloudShell; no local setup.  
Mirrors real-world flows for scalability and easy maintenance.

1. **API BLS Data → AWS S3**  
   Fetches BLS productivity and inflation data using my registered public API and bulk files (with a compliant custom User-Agent).  
   Compares file hashes to skip unchanged files, and stores results in Amazon S3.  
   **[View Notebook](s3-pipeline-bls-api-part1.ipynb)**

2. **API Request via AWS Lambda → S3**  
   Automates pulling BLS API data and dropping JSON into S3 on a monthly schedule using AWS Lambda Amazon EventBridge.
   Acts as a bridge between Part 1 and Part 3 data analysis.  
   **[View Script](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/lambda-api-s3-part2.py)**

   **Part Two Extention: Glue + Athena**  
   SQL Query S3-hosted BLS data via:  
   - **AWS Glue Data Catalog** – automated dataset crawling for schema management  
   - **Amazon Athena** – serverless SQL queries directly on S3 data  
   **[View Notebook - in process](glue-athena-part2-5a.ipynb)**

3. **Data Processing and Analysis**  
   Loads data from **S3** into a **Pandas notebook** (Kaggle) where it’s cleaned, merged, and transformed before producing summary reports.  
   Work is in progress to add **Amazon Athena** so the same datasets can be queried directly with SQL for faster, serverless analysis.  
   **[View Notebook](aws-data-pipeline-warehouse-part3.ipynb)**

4. **Automated Data Pipeline (Infrastructure as Code)**  
   Ship the stack with AWS CDK (Python) from CloudShell using no local setup.
   - Lambdas: ingest (BLS + DataUSA) and report (joins + summaries)
   - Storage: S3 with `raw/` → `processed/`
   - Events: EventBridge (daily) runs ingest; S3 `raw/` create → SQS → triggers report Lambda
   - S3 drops messages → SQS holds them → Lambda grabs when ready
     
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/iac-cloudshell-cdk-part4.ipynb)**

---
## AWS Tech Stack 
- S3 — store raw + processed BLS datasets
- Lambda — ingest API data and write to S3
- SQS — event-driven processing for reports (Part 4)
- CloudWatch Events — scheduled Lambda runs
- IAM — least-privilege roles for Lambda/S3/SQS
- CDK — infrastructure as code (deploy Lambda/S3/SQS)
- Glue Data Catalog — crawl/catalog datasets *(planned)*
- Athena — SQL on S3 via Glue catalog *(planned)*

### Security, SDKs & Data Sources
- **Secrets:** Kaggle Secrets (dev/demo); AWS Secrets Manager
- **SDKs:** Python 3.11, Pandas, Boto3 (AWS SDK for Python)
- **Sources:** BLS Public API + bulk files; DataUSA API
