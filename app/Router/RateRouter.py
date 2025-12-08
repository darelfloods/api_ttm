from fastapi import APIRouter, Depends, status, Request
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import RateController
from ..Schema import RateSchema, UserSchema

router = APIRouter()


@router.get("/all", tags=["Tarification"], response_model=list[RateSchema.Read])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await RateController.get_all(db)


@router.get("/active", tags=["Tarification"], response_model=list[RateSchema.Read])
async def get_active(
        db: Session = Depends(DatabaseSession.get_db)
):
    """Récupère uniquement les offres actives pour le site public"""
    return await RateController.get_active_rates(db)


@router.post("/add", tags=["Tarification"], status_code=status.HTTP_201_CREATED, response_model=RateSchema.Read)
async def add(
        rate: RateSchema.Create,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await RateController.add(db=db, rate=rate, current_user=current_user, request=request)


@router.put("/update/{id}", tags=["Tarification"])
async def update_rate(
        id: int,
        rate: RateSchema.Read,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await RateController.update_rate(db=db, rate=rate, id=id, current_user=current_user, request=request)


@router.delete("/delete/{id}", tags=["Tarification"])
async def delete_rate(
        id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await RateController.delete_rate(db=db, id=id, current_user=current_user, request=request)
