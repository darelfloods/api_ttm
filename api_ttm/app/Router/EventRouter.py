from fastapi import APIRouter, Depends, status, BackgroundTasks
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Schema import EventSchema
from ..Controller import EventController

router = APIRouter()


@router.get("/all", tags=["Evènement"])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await EventController.get_all(db)


@router.get("/get_by_timer/{start_at}/{end_at}", tags=["Evènement"])
async def get_by_timer(
        start_at: str,
        end_at: str,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await EventController.get_by_timer(db=db, start_at=start_at, end_at=end_at)


@router.get("/stat", tags=["Evènement"])
async def get_stat(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await EventController.get_stat(db)
