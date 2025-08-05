# AWS Data Engineering API: Four-Part Pipeline
This repo contains my solution to the Rearc Data Engineering Challenge.  
Each part of the project is documented separately:

- [Part 1: API Request into S3 database]
- [Part 2: AWS Glue Catalog]
- [Part 3: Data Transformation]
- [Part 4: Orchestration]

# Part 1 - API Request into S3 database
**Republish BLS Productivity Data into Amazon S3**

---
## 📌 Overview
Part 1 focuses on sourcing the **Bureau of Labor Statistics (BLS) Productivity dataset** and publishing it to an **AWS S3 bucket**. The process ensures the data is programmatically accessible and kept in sync with the official BLS source.

---
## ⚙️ Setup Instructions

### 1. Configure AWS CLI
Set up an AWS profile named `rearc-quest`:
aws configure --profile rearc-quest

###  Troubleshooting: 403 Errors & Glitchy User-Agent Header
When first attempting to fetch data from the [BLS site](https://www.bls.gov/), I ran into **403 Forbidden errors**. Based on BLS’s API access policy, requests must include a `User-Agent` header with valid contact info, or else automated traffic may be blocked.

---

## 🔑 BLS API Key Registration
I registered for a free BLS Public API key at [bls.gov](https://data.bls.gov/registrationEngine/) and received it by email.

Tested with Python:

```python
import requests, json

API_KEY = "YOUR_BLS_API_KEY"
payload = json.dumps({
    "registrationKey": API_KEY,
    "seriesid": ["PRS85006092"],
    "startyear": "2023",
    "endyear": "2024"
})
headers = {"Content-type": "application/json"}
r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", data=payload, headers=headers)

print(r.json()["status"])  # Expected: REQUEST_SUCCEEDED
```

## 🔐 Using `config.json` to Store Credentials
Instead of hardcoding my S3 bucket name and AWS profile directly in the script,  
I created a `config.json` file to keep sensitive info out of the codebase.

### Step 1: Create `config.json`

```json
{
  "bucket_name": "rearc-bls-scott-2025",
  "aws_profile": "rearc-quest"
}
```

# Part 2 - API Request into Athena 
https://honolulu-api.datausa.io/tesseract/data.jsonrecords?cube=acs_yg_total_population_1&drilldowns=Year%2CNation&locale=en&measures=Population

Each Athena query on my Honolulu dataset costs about $0.00005 — that’s 20,000 queries for just a dollar. For small JSON datasets, Athena is essentially free while letting us avoid the overhead of running a database cluster.
