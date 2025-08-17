# Four-Part AWS Data Engineering Pipeline
A four-stage pipeline on AWS — ingest → store → analyze → deploy-as-code.  
Uses S3, Lambda, SQS, EventBridge, Glue, IAM, Athena and CDK. Mirrors data pipeline flows for scalability and easy maintenance.  

## Pipeline Overview:
- One Lambda ingests data directly from the BLS and DataUSA APIs.  
- An S3 bucket stores raw and processed outputs.  
- Another Lambda joins the datasets, applies hashing for integrity/deduplication, and generates summary reports.  
- EventBridge triggers the ingest Lambda on a daily schedule.  
- When a new file lands in S3, it sends a notification to SQS.  
- The queue holds the event until the report Lambda processes it.  

---

## CI/CD with GitHub Actions  
> **Goal:** Create an automated deployment method that’s easier to troubleshoot and maintain once fully configured.

**CI/CD path (no SQS):**  
Git Push → GitHub Actions → Build & Test → Deploy to AWS  

**Runtime path (with SQS):**  
S3 Event → SQS Queue → Lambda → Athena  

*(Third deployment method — in process)*  
[**View CI/CD Workflows**](https://github.com/ScottySchmidt/AWS_DataEngineer_API)  

---

## 1. **API Data from BLS → AWS S3**  
   Fetches BLS productivity and inflation data using my registered public API and bulk files (with a compliant custom User-Agent).
    Compares file hashes to skip unchanged files, and stores results in Amazon S3.
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/01-ingest-apis-to-s3.ipynb)**

## 2. **API Request via AWS Lambda → S3**  
   Automates pulling API data from BLS and dropping JSON into S3 on a monthly schedule using AWS Lambda Amazon EventBridge. Acts as a bridge between Part 1 and Part 3 data analysis.  
   **[View Script](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/02-api-lambda-s3.py)**

#### 2.5 **Glue → Athena: Query S3-hosted Data**  
**Flow:** S3 (raw JSON) → Glue Crawler → Data Catalog → ETL → S3 (Parquet) → Athena → results (tables)  

- **AWS Glue Data Catalog** – automated dataset crawling for schema management  
- **Amazon Athena** – serverless SQL queries directly on S3 data  
 [View Notebook – In Process](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/02-glue-athena-extension.ipynb)

## 3. **Data Processing and Analysis**  
   Loads data from S3 into a Pandas notebook where it’s cleaned, merged, and transformed before producing summary reports. 
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/03-data-analytics-reports.ipynb)**

## 4. **Infrastructure as Code — AWS CDK Deployment**
   #### Method A: Python CDK (Local Jupyter Notebook)
   Runs directly from a Jupyter Notebook with minimal or no CloudShell usage.  
   This approach is easier to iterate on, test, and document.  
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/04-cdk-iac-python-local.ipynb)**
   
   #### Method B: Python CDK (AWS CloudShell)
   No local setup is required.  
   **[View Deployment Logs (sanitized)](https://github.com/ScottySchmidt/AWS_DataEngineer_API/tree/main/docs/part4)**
   
   This shows all the AWS resources that were created automatically when I deployed Part 4 with AWS CDK Cloud Shell Version:  
   <img width="600" height="400" alt="bls_pipeline_stack" src="https://github.com/user-attachments/assets/0540c36d-3b47-42f5-98ea-a2a08e2436ed" />

---
#### AWS Tech Stack  
- **Amazon S3** — buckets for both raw and processed BLS datasets  
- **AWS Lambda** — pulls API data and drops it into S3  
- **Amazon SQS** — queue for event-driven report processing (Part 4)  
- **Amazon EventBridge** — kicks off Lambda runs on a set schedule  
- **AWS IAM** — scoped-down roles for Lambda, S3, and SQS access  
- **AWS CDK** — spins up the stack (Lambda, S3, SQS) as code  
- **AWS Glue Data Catalog** — keeps S3 datasets organized with schemas  
- **Amazon Athena** — run SQL queries directly on S3 data via the Glue catalog  

#### Security, SDKs & Data Sources
- **Secrets:** Github and Kaggle Secrets; AWS Secrets Manager
- **SDKs:** Python, Pandas, Boto3 (AWS SDK for Python)
- **Sources:** BLS Public API + bulk files; DataUSA API
