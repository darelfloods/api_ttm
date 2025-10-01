from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from sqlalchemy import update, func

from ..Db.Model import AccountModel, RateModel
from ..Schema import AccountSchema, EventSchema, UserSchema
from . import EventController, UserController


################################### Read Function #####################################################################
async def get_all(db: Session):
    return db.query(AccountModel.Account).all()


async def get_by_id(db: Session, account_id: int):
    db_account = db.query(AccountModel.Account).filter(AccountModel.Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail=" Ce compte n'existe pas")
    return db_account


async def get_by_user_id(db: Session, user_id: int):
    db_account = db.query(AccountModel.Account).filter(AccountModel.Account.user_id == user_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail=" Cet utilisateur n'a pas de compte")
    return db_account


async def get_by_user_role(db: Session, role: str):
    accounts = []
    users = await UserController.get_by_role(db=db, role=role)
    for user in users:
        accounts.append(db.query(AccountModel.Account).filter(AccountModel.Account.user_id == user.id).first())
    return accounts


################################### Add Function #####################################################################
async def add(db: Session, account: AccountSchema.Create, user_id: int, request: Request):
    verif_account = db.query(AccountModel.Account).filter(AccountModel.Account.user_id == user_id).first()
    if verif_account:
        raise HTTPException(status_code=400, detail="Cet utilisateur possède déjà un compte")
    db_account = AccountModel.Account(
        credit=account.credit,
        subscription_date=account.subscription_date,
        user_id=account.user_id,
        rate_id=account.rate_id
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)

    event = EventSchema.Create(
        action="Création d'un compte",
        entity="accounts",
        entity_id=f"{db_account.id}",
        current_user_id=f"{user_id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return db_account


################################### Update Function ###################################################################
async def action_account(db: Session, account_id: int, request: Request, current_user: UserSchema.Read, activate: bool,
                         text_event: str):
    db_account = db.query(AccountModel.Account).filter(AccountModel.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail=" Ce compte n'existe pas")
    db_account.activate = activate
    db.commit()
    db.refresh(db_account)

    event = EventSchema.Create(
        action=text_event,
        entity="accounts",
        entity_id=f"{db_account.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)

    return db_account


async def subscribe_rate(db: Session, rate_id: int, account_id: int, request: Request):
    db_account = db.query(AccountModel.Account).filter(AccountModel.Account.id == account_id).first()
    if not db_account:
        raise HTTPException(status_code=404, detail=" Ce compte n'existe pas")
    db_rate = db.query(RateModel.Rate).filter(RateModel.Rate.id == rate_id).first()
    db_account.credit += db_rate.credit
    db_account.rate_id = db_rate.id
    db_account.subscription_date = func.now()
    db_account.updated_at = func.now()
    db.commit()
    db.refresh(db_account)

    event = EventSchema.Create(
        action="Souscription à une tarification",
        entity="accounts",
        entity_id=f"{db_account.id}",
        amount=db_rate.price,
        current_user_id=f"{db_account.user_id}"
    )
    await EventController.add(db=db, event=event, request=request)

    return db_account


async def spent(db: Session, account_id: int, credit: int, current_user: UserSchema.Read, request: Request):
    db_account = await get_by_id(db=db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Ce compte n'existe pas")
    if db_account.credit < credit:
        event = EventSchema.Create(
            action="Consommation de crédit: crédit insuffisant",
            entity="accounts",
            entity_id=f"{db_account.id}",
            current_user_id=f"{current_user.id}"
        )
        await EventController.add(db=db, event=event, request=request)
        raise HTTPException(status_code=404, detail="Ce compte n'a pas assez de crédit")
    db_account.credit -= credit
    db_account.updated_at = func.now()
    db.commit()
    db.refresh(db_account)

    event = EventSchema.Create(
        action="Consommation de crédit",
        entity="accounts",
        entity_id=f"{db_account.id}",
        amount=None,
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return db_account


################################### Delete Function #####################################################################
async def delete_account(db: Session, account_id: int, current_user: UserSchema.Read, request: Request):
    db_account = db.query(AccountModel.Account).filter(AccountModel.Account.id == account_id).first()
    if db_account is None:
        raise HTTPException(status_code=404, detail="Compte inexistant")
    db.delete(db_account)
    db.commit()

    event = EventSchema.Create(
        action="Suppression d'un compte",
        entity="accounts",
        entity_id=f"{db_account.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return {"msg": "Compte supprimé avec succès"}
