# Data Quest: Part 1  
**Republish BLS Productivity Data into Amazon S3**

---

## 📌 Overview
Part 1 of the Rearc Data Quest focuses on sourcing the **Bureau of Labor Statistics (BLS) Productivity dataset** and publishing it to an **AWS S3 bucket**. 
The process ensures the data is programmatically accessible and kept in sync with the official BLS source.

---

## ⚙️ Setup Instructions

### 1. Configure AWS CLI
Set up an AWS profile named `rearc-quest`:
```bash
aws configure --profile rearc-quest
