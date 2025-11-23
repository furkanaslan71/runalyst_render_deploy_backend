# app/core/scheduler.py

import asyncio
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

from app.models.run import Run  # Make sure your models are accessible

# --- Database Setup ---
# The scheduler runs in the same environment as the app, so it gets the same DB URL
DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def dispatch_one_pending_job():
    db = SessionLocal()
    try:
        job = db.query(Run).filter(Run.status == 'pending').with_for_update(skip_locked=True).first()

        if not job:
            print("Scheduler: No pending jobs found.")
            return

        print(f"Scheduler: Found pending job for run_id: {job.id}")
        job.status = 'dispatching'
        db.commit()
        print(f"Scheduler: Marked run_id {job.id} as 'dispatching'.")

        # --- BOILERPLATE: The "Dispatch" Logic ---
        print(f"--- SIMULATING DISPATCH for run_id {job.id} ---")
        # In the future, you would make a real HTTP request here.
        # requests.post(...)
        print(f"--- DISPATCH SIMULATION SUCCESSFUL for run_id {job.id} ---")

    except Exception as e:
        print(f"Scheduler: An error occurred during dispatch: {e}")
        db.rollback()
    finally:
        db.close()


async def run_dispatcher_periodically():
    print("Scheduler starting up...")
    while True:
        try:
            dispatch_one_pending_job()
        except Exception as e:
            # This ensures the scheduler itself doesn't crash if the dispatch logic fails
            print(f"Scheduler loop encountered an error: {e}")

        # Wait for 10 seconds before checking for new jobs again
        await asyncio.sleep(10)