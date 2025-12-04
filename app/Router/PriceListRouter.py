from fastapi import APIRouter, Depends, status, Request
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import PriceListController
from ..Schema import PriceListSchema, UserSchema

router = APIRouter()


@router.get("/all", tags=["Grille Tarifaire"], response_model=list[PriceListSchema.Read])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await PriceListController.get_all(db)


@router.get("/get_by_libelle/{libelle}", tags=["Grille Tarifaire"], response_model=PriceListSchema.Read)
async def get_by_libelle(
        libelle: str,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await PriceListController.get_price_list_by_libelle(db=db, libelle=libelle)


@router.post("/add", tags=["Grille Tarifaire"], response_model=PriceListSchema.Read)
async def add(
        price_list: PriceListSchema.Create,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await PriceListController.add(db=db, price_list=price_list, current_user=current_user, request=request)


@router.put("/update/{price_list_id}", tags=["Grille Tarifaire"])
async def update_price_list(
        price_list_id: int,
        price_list: PriceListSchema.Read,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await PriceListController.update_price_list(db=db, price_list=price_list, price_list_id=price_list_id,
                                                       current_user=current_user, request=request)


@router.delete("/delete/{price_list_id}", tags=["Grille Tarifaire"])
async def delete_price_list(
        price_list_id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await PriceListController.delete_price_list(db=db, price_list_id=price_list_id, current_user=current_user,
                                                       request=request)
