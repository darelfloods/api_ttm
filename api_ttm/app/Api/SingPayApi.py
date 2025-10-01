from fastapi import APIRouter, Depends, status, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from typing import Annotated
from jose import JWTError, jwt

from ..Middleware import IsAuthenticated, DatabaseSession
from ..Controller import AccountController
from core.config import settings
from ..Schema import TokenSchema
from ..Controller import UserController

router = APIRouter()


@router.get("/url_success/{token}/{rate_id}", tags=["Redirection SingPay"])
async def redirection_sing_pay(
        token: str,
        rate_id: int,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    current_user = await IsAuthenticated.get_current_user(token=token, db=db)
    account = await AccountController.get_by_user_id(db=db, user_id=current_user.id)
    await AccountController.subscribe_rate(db=db, rate_id=rate_id, account_id=account.id, request=request)

    target_url = "http://toctocmedoc.com/login"

    return RedirectResponse(target_url)


@router.get("/url_success_by_user_id/{user_id}/{rate_id}", tags=["Redirection SingPay"])
async def redirection_sing_pay_sign_out(
        user_id: int,
        rate_id: int,
        request: Request,
        db: Session = Depends(DatabaseSession.get_db)
):
    account = await AccountController.get_by_user_id(db=db, user_id=user_id)
    await AccountController.subscribe_rate(db=db, rate_id=rate_id, account_id=account.id, request=request)

    target_url = "http://toctocmedoc.com/login"

    return RedirectResponse(target_url)
