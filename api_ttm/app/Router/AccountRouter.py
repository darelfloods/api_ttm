from fastapi import APIRouter, Depends, status, Request
from typing import Annotated
from sqlalchemy.orm import Session

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import AccountController
from ..Schema import AccountSchema, UserSchema

router = APIRouter()


@router.get("/all", tags=["Comptes"], response_model=list[AccountSchema.Schema])
async def get_all(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.get_all(db)


@router.get("/get_by_role_admin", tags=["Comptes"], response_model=list[AccountSchema.Schema])
async def get_by_role_admin(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.get_by_user_role(db=db, role="ADMIN")


@router.get("/get_by_role_user", tags=["Comptes"], response_model=list[AccountSchema.Schema])
async def get_by_role_admin(
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.get_by_user_role(db=db, role="USER")


@router.get("/get_by_user_id/{user_id}", tags=["Comptes"], response_model=AccountSchema.Schema)
async def get_by_user_id(
        user_id: int,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.get_by_user_id(db=db, user_id=user_id)


@router.put("/subscribe_rate/{account_id}", tags=["Comptes"], response_model=AccountSchema.Schema)
async def subscribe_rate(
        account_id: int,
        rate_id: int,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.subscribe_rate(db=db, rate_id=rate_id, account_id=account_id, request=request)


@router.put("/spent/{account_id}", tags=["Comptes"], response_model=AccountSchema.Schema)
async def spent(
        account_id: int,
        credit: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.spent(db=db, account_id=account_id, credit=credit, current_user=current_user,
                                         request=request)


@router.put("/disable_account/{account_id}", tags=["Comptes"], response_model=AccountSchema.Schema)
async def disable_account(
        account_id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.action_account(db=db, account_id=account_id, request=request,
                                                  current_user=current_user, activate=False,
                                                  text_event="Désactivation du compte")


@router.put("/enable_account/{account_id}", tags=["Comptes"], response_model=AccountSchema.Schema)
async def enable_account(
        account_id: int,
        current_user: Annotated[UserSchema.Read, Depends(IsAuthenticated.get_current_user)],
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    return await AccountController.action_account(db=db, account_id=account_id, request=request,
                                                  current_user=current_user, activate=True,
                                                  text_event="Ré-activation du compte")
