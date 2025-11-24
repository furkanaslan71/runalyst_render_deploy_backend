# app/services/queue_service.py
import boto3
import os
import json

# These are automatically picked up by boto3 from the environment variables
# AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
AWS_REGION = os.environ.get("AWS_REGION")
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")


def send_message_to_queue(message_body: dict):
    if not SQS_QUEUE_URL:
        raise ValueError("SQS_QUEUE_URL is not set.")

    response = sqs_client.send_message(
        QueueUrl=SQS_QUEUE_URL,
        MessageBody=json.dumps(message_body)
    )
    return response