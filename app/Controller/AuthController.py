from fastapi import HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

from ..Db.Model import UserModel, AccountModel
from core.config import settings
from ..Schema import UserSchema, EventSchema
from . import EventController


def verify_password(plain_password, hashed_password):
    try:
        # Bcrypt a une limite de 72 octets pour les mots de passe
        # On tronque le mot de passe si nécessaire
        if len(plain_password.encode('utf-8')) > 72:
            plain_password = plain_password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
        return settings.pwd_context.verify(plain_password, hashed_password)
    except ValueError as e:
        # Si bcrypt échoue à cause de la limite de 72 octets, on retourne False
        print(f"ERREUR verify_password: {e}")
        return False


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


async def login(db: Session, username: str, password: str, request: Request):
    current_user = db.query(UserModel.User).filter(UserModel.User.email == username).first()

    if not current_user:
        print(f"INFO: user: {username} not existe")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Coordonnées incorrecte",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_account = db.query(AccountModel.Account).filter(AccountModel.Account.user_id == current_user.id).first()

    if not verify_password(password, current_user.password):
        if current_account and current_account.activate is False:
            print(f"INFO: user: {current_user.email}")
            event = EventSchema.Create(
                action="Authentification échoué",
                entity="users",
                entity_id=f"{current_user.id}",
                current_user_id=f"{current_user.id}"
            )
            await EventController.add(db=db, event=event, request=request)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Coordonnées incorrecte",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "email": current_user.email,
            "role": current_user.role
        },
        expires_delta=access_token_expires
    )
    print(f"INFO: user: {current_user.email}")
    event = EventSchema.Create(
        action="Authentification",
        entity="users",
        entity_id=f"{current_user.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    print(current_user.email)
    return {
        "token": {"access_token": access_token, "token_type": "bearer"},
        "user": UserSchema.Read(**vars(current_user))
    }


async def login_admin(db: Session, username: str, password: str, request: Request):
    current_user = db.query(UserModel.User).filter(UserModel.User.email == username).first()

    if not current_user:
        print(f"INFO: user: {username} not existe")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Coordonnées incorrecte",
            headers={"WWW-Authenticate": "Bearer"},
        )

    current_account = db.query(AccountModel.Account).filter(AccountModel.Account.user_id == current_user.id).first()

    if not verify_password(password, current_user.password):
        if current_account and current_account.activate is False:
            print(f"INFO: user: {current_user.email}")
            event = EventSchema.Create(
                action="Authentification admin échoué",
                entity="users",
                entity_id=f"{current_user.id}",
                current_user_id=f"{current_user.id}"
            )
            await EventController.add(db=db, event=event, request=request)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Coordonnées incorrecte",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if current_user.role == "USER":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Vous n'êtes pas autorisé à vous connecter",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "email": current_user.email,
            "role": current_user.role
        },
        expires_delta=access_token_expires
    )
    print(f"INFO: user: {current_user.email}")
    event = EventSchema.Create(
        action="Authentification admin",
        entity="users",
        entity_id=f"{current_user.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    print(current_user.email)
    return {
        "token": {"access_token": access_token, "token_type": "bearer"},
        "user": UserSchema.Read(**vars(current_user))
    }
