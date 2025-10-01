from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request, BackgroundTasks
from sqlalchemy import update, func
import random
import string

from ..Db.Model import UserModel
from ..Schema import UserSchema, AccountSchema, EventSchema
from . import AccountController, EventController
from core.config import settings
from ..Mailer import SendPassword


################################### Read Function #####################################################################
async def get_by_email(db: Session, email: str):
    user = db.query(UserModel.User).filter(UserModel.User.email == email).first()
    if user is not None:
        return UserSchema.Read(**vars(user))


async def get_all(db: Session):
    return db.query(UserModel.User).all()


async def get_by_role(db: Session, role: str):
    return db.query(UserModel.User).filter(UserModel.User.role == role).all()


################################### Add Function #####################################################################
async def add(db: Session, user: UserSchema.Create, request: Request):
    verif_user = await get_by_email(db=db, email=user.email)
    if verif_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    db_user = UserModel.User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        phone=user.phone,
        role=user.role,
        password=hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    db_account = AccountSchema.Create(
        credit=10,
        user_id=db_user.id
    )
    await AccountController.add(db=db, account=db_account, user_id=db_user.id, request=request)

    return db_user


################################### Update Function ###################################################################
async def recovery_password(db: Session, email: str, background_tasks: BackgroundTasks, request: Request):
    user = await get_by_email(db=db, email=email)
    if user is None:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")
    clear_password = generate_password()
    query = update(UserModel.User).where(UserModel.User.id == user.id).values(
        password=hash_password(clear_password),
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()

    event = EventSchema.Create(
        action="Réinitialisation du mot de passe",
        entity="users",
        entity_id=f"{user.id}",
        current_user_id=f"{user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    background_tasks.add_task(SendPassword.send_password(clear_password, email, user), password=clear_password,
                              to_email=user.email, user=user)
    return {"msg": "Mot de passe réinitialisé"}


async def update_password(db: Session, user_id: int, new_password: str, current_user: UserSchema.Read,
                          request: Request):
    query = update(UserModel.User).where(UserModel.User.id == user_id).values(
        password=hash_password(new_password),
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()

    event = EventSchema.Create(
        action="Modification du mot de passe",
        entity="users",
        entity_id=f"{user_id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return {"msg": "Mot de passe modifié avec succès"}


async def update_user(db: Session, user: UserSchema.Read, id: int, current_user: UserSchema.Read, request: Request):
    query = update(UserModel.User).filter(UserModel.User.id == id).values(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email,
        phone=user.phone,
        role=user.role,
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()

    event = EventSchema.Create(
        action="Modification d'un utilisateur",
        entity="users",
        entity_id=f"{id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)

    return {"msg": "Utilisateur modifié avec succès"}


################################### Delete Function #####################################################################
async def delete_user(db: Session, id: int, current_user: UserSchema.Read, request: Request):
    db_user = db.query(UserModel.User).filter(UserModel.User.id == id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Utilisateur inexistant")
    db_account = await AccountController.get_by_user_id(db=db, user_id=id)
    await AccountController.delete_account(db=db, account_id=db_account.id, current_user=current_user, request=request)
    db.delete(db_user)
    db.commit()
    return {"msg": "Utilisateur supprimé avec succès"}


################################### Function #####################################################################
def hash_password(password):
    return settings.pwd_context.hash(password)


def generate_password():
    characters = string.ascii_letters + string.digits + string.punctuation
    clear_password = ''.join(random.choice(characters) for _ in range(7))
    return clear_password

