# Data Quest: Part 1  
**Republish BLS Productivity Data into Amazon S3**

---

## 📌 Overview
Part 1 focuses on sourcing the **Bureau of Labor Statistics (BLS) Productivity dataset** and publishing it to an **AWS S3 bucket**. The process ensures the data is programmatically accessible and kept in sync with the official BLS source.

---

## ⚙️ Setup Instructions

### 1. Configure AWS CLI
Set up an AWS profile named `rearc-quest`:
```bash
aws configure --profile rearc-quest



###  Troubleshooting: 403 Errors & Glitchy User-Agent Header

When first attempting to fetch data from the [BLS site](https://www.bls.gov/), I ran into **403 Forbidden errors**. Based on BLS’s API access policy, requests must include a `User-Agent` header with valid contact info, or else automated traffic may be blocked.

---

##### Attempt 1: Custom User-Agent - Hard Way
I initially tried setting a `User-Agent` header manually like this:

```python
headers = {
    "User-Agent": "Mozilla/5.0 (compatible; ScottBot/1.0; +scott@email.com)"
}


## 🔐 Using `config.json` to Store Credentials

Instead of hardcoding my S3 bucket name and AWS profile directly in the script,  
I created a `config.json` file to keep sensitive info out of the codebase.

### Step 1: Create `config.json`

```json
{
  "bucket_name": "rearc-bls-scott-2025",
  "aws_profile": "rearc-quest"
}
