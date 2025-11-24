import asyncio
import json

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import logging
import boto3


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


from app.models.run import Run

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# SQS Client Setup
AWS_REGION = os.environ.get("AWS_REGION")
sqs_client = boto3.client("sqs", region_name=AWS_REGION)
SQS_QUEUE_URL = os.environ.get("SQS_QUEUE_URL")


def process_jobs_from_sqs():
    """
    Polls SQS for jobs, dispatches them, and deletes them from the queue.
    """
    if not SQS_QUEUE_URL:
        logging.error("Scheduler: SQS_QUEUE_URL is not set.")
        return

    # Ask SQS for up to 5 messages. Wait up to 5 seconds for a message.
    response = sqs_client.receive_message(
        QueueUrl=SQS_QUEUE_URL,
        MaxNumberOfMessages=5,
        WaitTimeSeconds=5
    )

    messages = response.get("Messages", [])
    if not messages:
        logging.info("Scheduler: No new messages in SQS queue.")
        return

    for message in messages:
        receipt_handle = message['ReceiptHandle']
        try:
            body = json.loads(message['Body'])
            run_id = body.get("run_id")

            logging.info(f"Scheduler: Found job in SQS for run_id: {run_id}")

            # --- BOILERPLATE DISPATCH LOGIC ---
            logging.info(f"--- SIMULATING DISPATCH for run_id {run_id} ---")

            # CRITICAL: If dispatch is successful, delete the message from the queue
            # so it isn't processed again.
            sqs_client.delete_message(
                QueueUrl=SQS_QUEUE_URL,
                ReceiptHandle=receipt_handle
            )
            logging.info(f"--- DISPATCH SUCCESSFUL, deleted message for run_id {run_id} ---")

        except Exception as e:
            logging.error(f"Scheduler: Failed to process message. It will reappear in queue. Error: {e}")
            # If we fail, we DON'T delete the message. SQS will make it visible again
            # after a "visibility timeout" for another worker to try.


def dispatch_one_pending_job():
    db = SessionLocal()
    try:
        job = db.query(Run).filter(Run.status == 'pending').with_for_update(skip_locked=True).first()

        if not job:
            logging.info("Scheduler: No pending jobs found.")
            #print("Scheduler: No pending jobs found.")
            return

        print(f"Scheduler: Found pending job for run_id: {job.id}")
        job.status = 'dispatching'
        db.commit()
        print(f"Scheduler: Marked run_id {job.id} as 'dispatching'.")

        # BOILERPLATE
        print(f"--- SIMULATING DISPATCH for run_id {job.id} ---")
        # Later the real HTTP request here.
        # requests.post(...)
        print(f"--- DISPATCH SIMULATION SUCCESSFUL for run_id {job.id} ---")

    except Exception as e:
        #print(f"Scheduler: An error occurred during dispatch: {e}")
        logging.info(f"Scheduler: An error occurred during dispatch: {e}")
        db.rollback()
    finally:
        db.close()


async def run_dispatcher_periodically():
    logging.info("Scheduler starting up...")
    while True:
        try:
            process_jobs_from_sqs()
        except Exception as e:
            logging.error(f"Scheduler loop encountered an error: {e}")

        await asyncio.sleep(10)