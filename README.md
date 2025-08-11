# Four-Part AWS Data Engineering Pipeline
This repo showcases a four-stage AWS data pipeline—ingest → store → analyze → deploy as code. It’s **CI/CD-ready** and uses **Amazon S3, AWS Lambda, Amazon SQS, Amazon EventBridge (schedule), and the AWS CDK**. The project mirrors real-world flows—from raw ingestion to automated infrastructure—for scalability, maintainability, and automation. *Future extensions:* Amazon Athena, AWS Glue, and Amazon RDS.

1. **API BLS Data → AWS S3**  
   Fetches BLS productivity and inflation data via the public API and bulk files (with a compliant custom `User-Agent`).  
   Compares file hashes to skip unchanged files, and stores results in Amazon S3.  
   **[View Notebook](s3-pipeline-bls-api-part1.ipynb)**

2. **API Request via AWS Lambda → S3**  
   Automates pulling BLS data via their API and dropping JSON into S3 on demand or on a schedule.  
   Acts as the ingestion bridge between Part 1 (bulk/static) and Part 3 (analysis).  
   **[View Script](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/lambda_bls_api_part2.py)**

 2.5A **Glue + Athena**
      Query S3-hosted BLS data via **AWS Glue Data Catalog** and **Amazon Athena**.  
      **[View Notebook](glue-athena-part2-5a.ipynb)**

3. **Data Processing and Analysis**  
   Loads data from **S3** into a **Pandas notebook** (Kaggle) where it’s cleaned, merged, and transformed before producing summary reports.  
   Work is in progress to add **Amazon Athena** so the same datasets can be queried directly with SQL for faster, serverless analysis.  
   **[View Notebook](aws-data-pipeline-warehouse-part3.ipynb)**


4. **Automated Data Pipeline (Infrastructure as Code)**  
   Provisions the entire stack with **AWS CDK (Python)** for reproducible, one-command deploys via **CloudFormation**. Deployed from **AWS CloudShell** to skip local setup.  
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/iac-cloudshell-cdk-part4.ipynb)**

   **Resources**
   - Lambdas: **ingest** (BLS + DataUSA) and **report** (joins + summaries)
   - **S3** bucket with **raw/** and **processed/** prefixes (landing → curated)
   - **SQS** queue for change notifications

   **Event wiring**
   - **S3 ObjectCreated** (raw/) → send message to **SQS**
   - **SQS** message → triggers **report** Lambda (event source mapping)
   - **Amazon EventBridge (schedule)** → runs **ingest** Lambda daily

   **Operations**
   - Env vars for bucket name, endpoints, and keys (e.g., `BUCKET_NAME`, `BLS_BASE_URL`, `POP_API`)
   - Observability via **CloudWatch Logs** (verify runs, debug)
   - `cdk synth && cdk deploy --require-approval never` (CDK → CloudFormation)


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
