import json
import os
import boto3
import uuid
import re
import urllib.parse
from datetime import datetime
from PyPDF2 import PdfReader

# AWS Clients
s3 = boto3.client('s3')
dynamodb = boto3.resource('dynamodb')
ses = boto3.client('ses')

# Environment Variables
DYNAMODB_TABLE = os.environ.get('DYNAMODB_TABLE')

SES_SENDER_EMAIL = os.environ.get(
    'SES_SENDER_EMAIL'
)

SES_RECIPIENT_EMAIL = os.environ.get(
    'SES_RECIPIENT_EMAIL'
)

table = dynamodb.Table(DYNAMODB_TABLE)


def lambda_handler(event, context):

    try:

        print("LAMBDA STARTED")

        bucket = event['Records'][0]['s3']['bucket']['name']

        key = event['Records'][0]['s3']['object']['key']

        key = urllib.parse.unquote_plus(key)

        print(f"Bucket: {bucket}")
        print(f"Key: {key}")

        # Download PDF locally
        download_path = f"/tmp/{uuid.uuid4()}.pdf"

        s3.download_file(
            bucket,
            key,
            download_path
        )

        print("PDF Downloaded")

        # Extract text from PDF
        text = extract_text_from_pdf(download_path)

        print("TEXT EXTRACTED")
        print(text)

        # Extract resume details
        resume_data = extract_resume_details(text)

        print(resume_data)

        # Store in DynamoDB
        store_resume(resume_data, bucket, key)

        # Send email
        send_email(resume_data)

        return {
            'statusCode': 200,
            'body': json.dumps(
                'Resume processed successfully'
            )
        }

    except Exception as e:

        print("ERROR OCCURRED")
        print(str(e))

        raise e


def extract_text_from_pdf(pdf_path):

    reader = PdfReader(pdf_path)

    text = ""

    for page in reader.pages:
        text += page.extract_text()

    return text


def extract_resume_details(text):

    email = extract_email(text)

    phone = extract_phone(text)

    skills = extract_skills(text)

    name = text.split('\n')[0]

    return {
        'resume_id': str(uuid.uuid4()),
        'name': name,
        'email': email,
        'phone': phone,
        'skills': skills,
        'raw_text': text
    }


def extract_email(text):

    match = re.search(
        r'[\w\.-]+@[\w\.-]+',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_phone(text):

    match = re.search(
        r'\+?\d[\d -]{8,12}\d',
        text
    )

    return match.group(0) if match else "Not Found"


def extract_skills(text):

    predefined_skills = [

        'AWS',
        'Python',
        'Docker',
        'Kubernetes',
        'Jenkins',
        'Linux',
        'Terraform',
        'Git',
        'SQL',
        'Java'
    ]

    found_skills = []

    for skill in predefined_skills:

        if skill.lower() in text.lower():
            found_skills.append(skill)

    return found_skills


def store_resume(
    resume_data,
    bucket,
    key
):

    item = {

        'resume_id': resume_data['resume_id'],

        'name': resume_data['name'],

        'email': resume_data['email'],

        'phone': resume_data['phone'],

        'skills': resume_data['skills'],

        's3_path': f's3://{bucket}/{key}',

        'processed_timestamp':
        datetime.now().isoformat()
    }

    table.put_item(Item=item)

    print("Stored in DynamoDB")


def send_email(resume_data):

    body = f"""
Resume Processed Successfully

Name: {resume_data['name']}

Email: {resume_data['email']}

Phone: {resume_data['phone']}

Skills:
{', '.join(resume_data['skills'])}
"""

    response = ses.send_email(

        Source=SES_SENDER_EMAIL,

        Destination={
            'ToAddresses': [
                SES_RECIPIENT_EMAIL
            ]
        },

        Message={
            'Subject': {
                'Data': 'Resume Processed'
            },
            'Body': {
                'Text': {
                    'Data': body
                }
            }
        }
    )

    print(response)