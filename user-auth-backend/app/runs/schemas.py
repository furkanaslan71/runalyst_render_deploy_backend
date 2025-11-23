from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Any

# --- Input Schema ---
# This defines what the frontend must send when confirming an upload.
class RunCreateIn(BaseModel):
    video_path: str
    title: Optional[str] = None

# --- Output Schema ---
# This defines what our API will return after successfully creating a run.
class RunOut(BaseModel):
    id: int
    title: Optional[str]
    video_path: str
    created_at: datetime
    user_id: int
    analysis_results: Optional[dict]

    class Config:
        from_attributes = True # This allows Pydantic to read data from ORM models