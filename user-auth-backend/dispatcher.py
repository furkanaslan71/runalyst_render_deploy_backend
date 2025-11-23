# dispatcher.py

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import requests  # We'll need this to make HTTP requests later

from app.models.run import Run

# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.environ.get("DATABASE_URL")
# This will be the URL of your ML service on the university machines
ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL", "http://university-gpu-machine/analyze")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

# --- Database Setup ---
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def dispatch_one_pending_job():
    """
    Finds one 'pending' job in the database, marks it as 'dispatching',
    and sends it to the ML service.
    """
    db = SessionLocal()
    try:
        # Atomically find and lock the next pending job.
        # This prevents two dispatcher instances from grabbing the same job.
        job = db.query(Run).filter(Run.status == 'pending').with_for_update(skip_locked=True).first()

        if not job:
            print("No pending jobs found. Exiting.")
            return

        print(f"Found pending job for run_id: {job.id}")

        # --- Mark the job as 'dispatching' so it's not picked up again ---
        job.status = 'dispatching'
        db.commit()
        print(f"Marked run_id {job.id} as 'dispatching'.")

        # --- BOILERPLATE: Send the job to the ML service ---
        # In a real application, you would make an HTTP POST request here.
        # The body would contain the information the ML service needs, like
        # the video URL and a webhook URL to call when it's done.

        payload_to_send = {
            "run_id": job.id,
            "video_path": job.video_path,
            "callback_url": "https://your-render-app.onrender.com/runs/callback"  # Example
        }

        print(f"--- SIMULATING DISPATCH ---")
        print(f"Sending POST request to: {ML_SERVICE_URL}")
        print(f"With payload: {payload_to_send}")

        # In the future, you would uncomment this:
        # response = requests.post(ML_SERVICE_URL, json=payload_to_send, timeout=10)
        # response.raise_for_status() # Raise an exception for HTTP errors

        print(f"--- DISPATCH SIMULATION SUCCESSFUL for run_id {job.id} ---")

    except Exception as e:
        print(f"An error occurred during dispatch: {e}")
        # If the dispatch failed, you might want to roll back and set the status back to 'pending'
        # For simplicity, we'll leave it as 'dispatching' for now.
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    dispatch_one_pending_job()