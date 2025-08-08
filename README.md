# AWS Data Engineering – BLS API Pipeline
This repository contains a multi-part AWS data engineering pipeline that ingests, processes, and stores data from the U.S. Bureau of Labor Statistics (BLS) and other sources.

## Project Parts
1. **Part 1 – BLS Data to S3**  
   Fetches BLS productivity and inflation data using both the BLS Public API and direct file downloads with a custom `User-Agent`.  
   Compares file hashes to avoid re-uploading unchanged files, and stores results in Amazon S3.  
   [View Notebook](s3-pipeline-bls-api-part1.ipynb)

2. **Part 2 – API Request via AWS Lambda → S3** *(implemented on AWS, not yet uploaded to GitHub)*

3. **Part 3 – Data Processing and Analysis**  
   Loads the stored data from S3 into Pandas for cleaning, transformation, and analytical reporting.  
   [View Notebook](aws-data-pipeline-warehouse-part3.ipynb)

4. **Part 4 – Automated Data Pipeline (IaC)** *(coming soon)*

---
More details will be added once all parts are completed and documented.
