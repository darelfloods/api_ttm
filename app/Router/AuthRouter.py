from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


from ..Controller import AuthController
from ..Middleware import DatabaseSession
from ..Schema import AuthSchema

router = APIRouter()


@router.post("/login", tags=["Authentication"], response_model=AuthSchema.Authentication)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(DatabaseSession.get_db)):
    return await AuthController.login(db, username=form_data.username, password=form_data.password, request=request)


@router.post("/login_admin", tags=["Authentication"], response_model=AuthSchema.Authentication)
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(),
                db: Session = Depends(DatabaseSession.get_db)):
    return await AuthController.login_admin(db, username=form_data.username, password=form_data.password, request=request)
