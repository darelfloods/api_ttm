from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from sqlalchemy import update, func

from ..Db.Model import RateModel
from ..Schema import RateSchema, EventSchema, UserSchema
from . import EventController


################################### Read Function #####################################################################
async def get_all(db: Session):
    return db.query(RateModel.Rate).all()


async def get_active_rates(db: Session):
    """Récupère uniquement les tarifs actifs, triés par display_order"""
    return db.query(RateModel.Rate).filter(
        RateModel.Rate.is_active == True
    ).order_by(RateModel.Rate.display_order.asc()).all()


################################### Add Function #####################################################################
async def add(db: Session, rate: RateSchema.Create, current_user: UserSchema.Read, request: Request):
    db_rate = RateModel.Rate(
        libelle=rate.libelle,
        price=rate.price,
        credit=rate.credit,
        image_url=rate.image_url,
        badge_icon=rate.badge_icon,
        badge_text=rate.badge_text,
        is_popular=rate.is_popular,
        display_order=rate.display_order,
        is_active=rate.is_active
    )
    db.add(db_rate)
    db.commit()
    db.refresh(db_rate)

    event = EventSchema.Create(
        action="Création d'une tarification",
        entity="rates",
        entity_id=f"{db_rate.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return db_rate


################################### Update Function #####################################################################
async def update_rate(db: Session, rate: RateSchema.Read, id: int, current_user: UserSchema.Read, request: Request):
    query = update(RateModel.Rate).where(RateModel.Rate.id == id).values(
        libelle=rate.libelle,
        price=rate.price,
        credit=rate.credit,
        image_url=rate.image_url,
        badge_icon=rate.badge_icon,
        badge_text=rate.badge_text,
        is_popular=rate.is_popular,
        display_order=rate.display_order,
        is_active=rate.is_active,
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()

    event = EventSchema.Create(
        action="Modification d'une tarification",
        entity="rates",
        entity_id=f"{id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return {"msg": "Tarif modifié avec succès"}


################################### Delete Function #####################################################################
async def delete_rate(db: Session, id: int, current_user: UserSchema, request: Request):
    db_rate = db.query(RateModel.Rate).filter(RateModel.Rate.id == id).first()
    if db_rate is None:
        raise HTTPException(status_code=404, detail="Tarification inexistante")
    db.delete(db_rate)
    db.commit()

    event = EventSchema.Create(
        action="Suppression d'une tarification",
        entity="rates",
        entity_id=f"{id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)

    return {"msg": "Tarif supprimé avec succès"}
