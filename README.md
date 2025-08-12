# Four-Part AWS Data Engineering Pipeline
A four-stage pipeline on AWS — ingest → store → analyze → deploy-as-code.  
Uses S3, Lambda, SQS, EventBridge, Glue, IAM, Athena and CDK.  Deployed from AWS CloudShell; no local setup.  
Mirrors data pipeline flows for scalability and easy maintenance.

1. **API Data from BLS → AWS S3**  
   Fetches BLS productivity and inflation data using my registered public API and bulk files (with a compliant custom User-Agent).
    Compares file hashes to skip unchanged files, and stores results in Amazon S3.
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/01-ingest-apis-to-s3.ipynb)**

3. **API Request via AWS Lambda → S3**  
   Automates pulling API data from BLS and dropping JSON into S3 on a monthly schedule using AWS Lambda Amazon EventBridge. Acts as a bridge between Part 1 and Part 3 data analysis.  
   **[View Script](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/02-lambda-api-s3.py)**

   #### Part2.5 Addition Glue → Athena: Query S3 hosted Data 
     Flow: S3 (raw JSON) → Glue Crawler → Data Catalog → ETL → S3 (Parquet) → Athena → results (tables)
    - AWS Glue Data Catalog – automated dataset crawling for schema management  
    - Amazon Athena – serverless SQL queries directly on S3 data  
    **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/02-glue-athena-extension.ipynb)**

4. **Data Processing and Analysis**  
   Loads data from S3 into a Pandas notebook where it’s cleaned, merged, and transformed before producing summary reports.
   Work is in progress to add Amazon Athena so the same datasets can be queried directly with SQL for faster, serverless analysis.  
   **[View Notebook](https://github.com/ScottySchmidt/AWS_DataEngineer_API/blob/main/03-data-analytics-reports.ipynb)**

 5. **Infrastructure as Code — AWS CDK**  
    Deploy the pipeline with AWS CDK (Python) from CloudShell. No local setup is needed.
    One Lambda pulls data from BLS and DataUSA, and another joins the datasets to create summary reports.
    An S3 bucket stores both raw data and the processed outputs.
    EventBridge runs the ingest Lambda on a daily schedule.
    When a new file lands in S3, it sends a notification to SQS.
    The queue holds the event until the report Lambda picks it up and processes it.
   **[View Logs Folder](https://github.com/ScottySchmidt/AWS_DataEngineer_API/tree/main/docs/part4)**

---
### AWS Tech Stack  
- **Amazon S3** — buckets for both raw and processed BLS datasets  
- **AWS Lambda** — pulls API data and drops it into S3  
- **Amazon SQS** — queue for event-driven report processing (Part 4)  
- **Amazon EventBridge** — kicks off Lambda runs on a set schedule  
- **AWS IAM** — scoped-down roles for Lambda, S3, and SQS access  
- **AWS CDK** — spins up the stack (Lambda, S3, SQS) as code  
- **AWS Glue Data Catalog** — keeps S3 datasets organized with schemas  
- **Amazon Athena** — run SQL queries directly on S3 data via the Glue catalog  

### Security, SDKs & Data Sources
- **Secrets:** Kaggle Secrets; AWS Secrets Manager
- **SDKs:** Python, Pandas, Boto3 (AWS SDK for Python)
- **Sources:** BLS Public API + bulk files; DataUSA API
