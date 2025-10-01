from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status, Request
from typing import Annotated
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from core.config import settings
from ..Middleware.DatabaseSession import get_db
from ..Schema import TokenSchema
from ..Controller import UserController

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Vous n'êtes pas autorisé à effectuer cette action",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        email: str = payload.get("email")
        if email is None:
            raise credentials_exception
        token_data = TokenSchema.TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = await UserController.get_by_email(db=db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user
