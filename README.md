# Automated AWS Resume Analyzer

A serverless cloud-native resume processing system built using AWS services. This project automatically processes uploaded PDF resumes, extracts candidate information, stores structured data in DynamoDB, and sends automated email notifications.

---

# Architecture Overview

<img width="1536" height="1024" alt="Architecture" src="https://github.com/user-attachments/assets/bb466661-a3f4-4c7b-a6b2-a5f4064ba6e8" />


---

# Features

- Serverless event-driven architecture
- Automatic PDF resume processing
- Resume text extraction using PyPDF2
- Candidate detail extraction using Regex
- Stores extracted data in DynamoDB
- Sends email notifications using Amazon SES
- CloudWatch monitoring and logging
- Scalable AWS-managed infrastructure

---

# AWS Services Used

- AWS Lambda
- Amazon S3
- Amazon DynamoDB
- Amazon SES
- AWS IAM
- Amazon CloudWatch

---

# Technologies Used

- Python 3.12
- PyPDF2
- Regex
- Boto3
- Git & GitHub

---

# Project Workflow

```text
User Uploads Resume PDF
            ↓
Amazon S3 Bucket
            ↓
S3 Trigger Invokes Lambda
            ↓
Lambda Downloads Resume
            ↓
PyPDF2 Extracts Text
            ↓
Regex Extracts:
- Name
- Email
- Phone
- Skills
            ↓
Store Details in DynamoDB
            ↓
Send Email Notification via SES
            ↓
CloudWatch Logs Monitoring
```

---

# Project Structure

```text
automated-aws-resume-analyzer/
│
├── lambda_function.py
├── README.md
├── architecture.png
├── sample_resume.pdf
│
├── screenshots/
│   ├── s3-trigger.png
│   ├── lambda-function.png
│   ├── dynamodb-data.png
│   ├── ses-email.png
│   └── cloudwatch-logs.png
│
└── layer/
    └── pypdf2-layer.zip
```

---

# Setup Instructions

## 1. Create S3 Bucket

Create an S3 bucket and add a folder:

```text
incoming/
```

This folder will store uploaded resume PDFs.

---

## 2. Create DynamoDB Table

Create a table:

```text
ResumeData
```

Partition key:

```text
resume_id (String)
```

---

## 3. Verify Email in Amazon SES

Verify sender and recipient email addresses in SES.

Example:

```text
your_email@gmail.com
```

---

## 4. Create IAM Role

Attach the following permissions:

```text
AmazonS3ReadOnlyAccess
AmazonDynamoDBFullAccess
AmazonSESFullAccess
AWSLambdaBasicExecutionRole
```

---

## 5. Create Lambda Function

Runtime:

```text
Python 3.12
```

Attach the IAM role created earlier.

---

## 6. Configure Lambda Environment Variables

Add:

```text
DYNAMODB_TABLE = ResumeData
SES_SENDER_EMAIL = your_email@gmail.com
SES_RECIPIENT_EMAIL = your_email@gmail.com
```

---

## 7. Add S3 Trigger

Configure S3 trigger:

```text
Bucket Event Type: PUT
Prefix: incoming/
```

---

## 8. Create Lambda Layer

Install dependency locally:

```bash
mkdir python
pip install PyPDF2 -t python/
powershell Compress-Archive python pypdf2-layer.zip
```

Upload ZIP as Lambda Layer and attach it to the function.

---

## 9. Deploy Lambda Code

Upload the provided `lambda_function.py` code to AWS Lambda and deploy.

---

## 10. Upload Resume PDF

Upload PDF resumes into:

```text
incoming/
```

Example:

```text
incoming/sample_resume.pdf
```

---

# Extracted Resume Details

The system extracts:

- Candidate Name
- Email Address
- Phone Number
- Skills
- Raw Resume Text
- S3 File Path
- Processing Timestamp

---

# Sample DynamoDB Record

```json
{
  "resume_id": "uuid",
  "name": "John Doe",
  "email": "john.doe@gmail.com",
  "phone": "+1 9876543210",
  "skills": [
    "AWS",
    "Python",
    "Docker"
  ],
  "s3_path": "s3://bucket/incoming/resume.pdf"
}
```

---

# Cloud Skills Demonstrated

- AWS Serverless Architecture
- Event-Driven Systems
- Cloud Automation
- AWS IAM & Security
- Lambda Functions
- Cloud Monitoring
- NoSQL Database Integration
- Object Storage Management
- Email Notification Systems

---

# Future Improvements

- Resume ranking system
- AI-based skill analysis
- API Gateway integration
- Frontend dashboard
- Multi-user support
- Step Functions workflow
- Resume scoring system

---

# Author

Swaraj Kawade

---

# License

This project is created for educational and portfolio purposes.
