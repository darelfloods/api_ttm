from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from fastapi import HTTPException, Request
from sqlalchemy import update, func

from ..Db.Model import PriceListModel
from ..Schema import PriceListSchema, EventSchema, UserSchema
from . import EventController


################################### Read Function #####################################################################
async def get_all(db: Session):
    return db.query(PriceListModel.PriceList).all()


async def get_price_list_by_libelle(db: Session, libelle: str):
    return db.query(PriceListModel.PriceList).filter(PriceListModel.PriceList.libelle == libelle).first()


################################### Add Function #####################################################################
async def add(db: Session, price_list: PriceListSchema.Create, current_user: UserSchema.Read, request: Request):
    db_price_list = PriceListModel.PriceList(
        libelle=price_list.libelle,
        credit=price_list.credit,
    )
    db.add(db_price_list)
    db.commit()
    db.refresh(db_price_list)

    event = EventSchema.Create(
        action="Création d'une grille tarifaire",
        entity="pricelists",
        entity_id=f"{db_price_list.id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return db_price_list


################################### Update Function #####################################################################
async def update_price_list(db: Session, price_list: PriceListSchema.Read, price_list_id: int,
                            current_user: UserSchema.Read, request: Request):
    query = update(PriceListModel.PriceList).where(PriceListModel.PriceList.id == price_list_id).values(
        libelle=price_list.libelle,
        credit=price_list.credit,
        updated_at=func.now()
    )
    db.execute(query)
    db.commit()

    event = EventSchema.Create(
        action="Modification d'une grille tarifaire",
        entity="pricelists",
        entity_id=f"{price_list_id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return {"msg": "Grille tarifaire modifié avec succès"}


################################### Delete Function #####################################################################
async def delete_price_list(db: Session, price_list_id: int, current_user: UserSchema.Read, request: Request):
    db_price_list = db.query(PriceListModel.PriceList).filter(PriceListModel.PriceList.id == price_list_id).first()
    if db_price_list is None:
        raise HTTPException(status_code=404, detail="Grille tarifaire inexistante")
    db.delete(db_price_list)
    db.commit()

    event = EventSchema.Create(
        action="Suppression d'une grille tarifaire",
        entity="pricelists",
        entity_id=f"{price_list_id}",
        current_user_id=f"{current_user.id}"
    )
    await EventController.add(db=db, event=event, request=request)
    return {"msg": "Grille tarifaire supprimé avec succès"}
