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


async def get_all(db: Session, limit: int = 1000):
    # Optimisation : charger tous les événements et les relations en batch pour éviter le problème N+1
    # Limiter les résultats pour améliorer les performances (1000 par défaut, ajustable)
    db_events = db.query(EventModel.Event).order_by(EventModel.Event.date_time.desc()).limit(limit).all()
    
    if not db_events:
        return []
    
    # Collecter tous les IDs uniques
    user_ids = set()
    account_ids = set()
    price_list_ids = set()
    rate_ids = set()
    
    for event in db_events:
        if event.current_user_id:
            user_ids.add(event.current_user_id)
        try:
            if event.entity == "users" and event.entity_id:
                user_ids.add(int(event.entity_id))
            elif event.entity == "accounts" and event.entity_id:
                account_ids.add(int(event.entity_id))
            elif event.entity == "pricelists" and event.entity_id:
                price_list_ids.add(int(event.entity_id))
            elif event.entity == "rates" and event.entity_id:
                rate_ids.add(int(event.entity_id))
        except (ValueError, TypeError):
            continue
    
    # Charger toutes les relations en batch
    users_dict = {user.id: user for user in db.query(UserModel.User).filter(UserModel.User.id.in_(user_ids)).all()} if user_ids else {}
    accounts_dict = {acc.id: acc for acc in db.query(AccountModel.Account).filter(AccountModel.Account.id.in_(account_ids)).all()} if account_ids else {}
    price_lists_dict = {pl.id: pl for pl in db.query(PriceListModel.PriceList).filter(PriceListModel.PriceList.id.in_(price_list_ids)).all()} if price_list_ids else {}
    rates_dict = {rate.id: rate for rate in db.query(RateModel.Rate).filter(RateModel.Rate.id.in_(rate_ids)).all()} if rate_ids else {}
    
    # Mapper les relations aux événements
    for event in db_events:
        # Toujours charger l'utilisateur courant
        event.current_user = users_dict.get(event.current_user_id)
        
        # Charger l'entité selon son type
        try:
            entity_id = int(event.entity_id) if event.entity_id else None
            if entity_id:
                if event.entity == "users":
                    event.current_entity = users_dict.get(entity_id)
                elif event.entity == "accounts":
                    event.current_entity = accounts_dict.get(entity_id)
                elif event.entity == "pricelists":
                    event.current_entity = price_lists_dict.get(entity_id)
                elif event.entity == "rates":
                    event.current_entity = rates_dict.get(entity_id)
                else:
                    event.current_entity = None
        except (ValueError, TypeError):
            event.current_entity = None
    
    return db_events


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
