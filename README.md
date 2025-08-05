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

To keep sensitive information (like my AWS bucket name and profile) **out of the codebase**,  
I created a `config.json` file. This allows the Python script to read values dynamically without hardcoding them.

---

### 📂 Security Addition: Create `config.json`

In the project root, I created a file called `config.json`:
This helps hide confidential information:
```json
{
  "bucket_name": "*****-scott-2025",
  "aws_profile": "*****-quest"
}

