from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps.db import get_db
from app.deps.auth import get_current_user
from app.models.user import User
from app.models.run import Run
from .schemas import RunCreateIn, RunOut

router = APIRouter(prefix="/runs", tags=["runs"])


@router.post("/", response_model=RunOut, status_code=status.HTTP_201_CREATED)
def create_run_record(
        payload: RunCreateIn,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    try:
        new_run = Run(
            video_path=payload.video_path,
            title=payload.title,
            user_id=current_user.id
        )

        db.add(new_run)
        db.commit()
        db.refresh(new_run)

        return new_run

    except Exception as e:
        db.rollback()
        # in prod, log it
        print(f"Error creating run record: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create run record in the database."
        )