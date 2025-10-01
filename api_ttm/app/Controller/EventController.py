from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, BackgroundTasks, Request
from sqlalchemy import update, func
from datetime import datetime


from ..Db.Model import EventModel, UserModel, AccountModel, PriceListModel, RateModel
from ..Schema import EventSchema


################################### Read Function #####################################################################
async def get_stat(db: Session):
    tab = ["Authentification", "Création d'un compte", "Disponibilité d'un produit", "Réservation d'un produit",
           "Souscription à une tarification", "Consommation de crédit"]
    return db.query(EventModel.Event).filter(EventModel.Event.action.in_(tab)).all()


async def get_by_timer(db: Session, start_at: str, end_at: str):
    tab = ["Authentification", "Création d'un compte", "Disponibilité d'un produit", "Réservation d'un produit",
           "Souscription à une tarification", "Consommation de crédit"]
    start_date = datetime.strptime(start_at, "%Y-%m-%d")
    end_date = datetime.strptime(end_at, "%Y-%m-%d")
    return db.query(EventModel.Event).filter(
        EventModel.Event.action.in_(tab),
        EventModel.Event.date_time.between(start_date, end_date)
    ).all()


async def get_all(db: Session):
    events = []
    db_events = db.query(EventModel.Event).all()
    for event in db_events:
        match event.entity:
            case "users":
                event.current_entity = db.query(UserModel.User).filter(UserModel.User.id == event.entity_id).first()
                event.current_user = db.query(UserModel.User).filter(UserModel.User.id == event.current_user_id).first()
            case "accounts":
                event.current_entity = (db.query(AccountModel.Account)
                                        .filter(AccountModel.Account.id == event.entity_id).first())
                event.current_user = db.query(UserModel.User).filter(UserModel.User.id == event.current_user_id).first()
            case "pricelists":
                event.current_entity = (db.query(PriceListModel.PriceList)
                                        .filter(PriceListModel.PriceList.id == event.entity_id).first())
                event.current_user = db.query(UserModel.User).filter(UserModel.User.id == event.current_user_id).first()
            case "rates":
                event.current_entity = db.query(RateModel.Rate).filter(RateModel.Rate.id == event.entity_id).first()
                event.current_user = db.query(UserModel.User).filter(UserModel.User.id == event.current_user_id).first()
        events.append(event)
    return events


################################### Add Function #####################################################################
async def add(db: Session, event: EventSchema.Create, request: Request):
    db_event = EventModel.Event(
        ip_address=f"{request.client.host}",
        action=event.action,
        entity=event.entity,
        entity_id=event.entity_id,
        amount=event.amount,
        current_user_id=event.current_user_id
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
