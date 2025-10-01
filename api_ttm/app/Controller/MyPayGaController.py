from sqlalchemy.orm import Session
from datetime import datetime
from fastapi import Request

from ..Schema import UserSchema
from ..Controller import AccountController


################################### Read Function #####################################################################
async def get_all():
    return {"msg": "ça passe"}


################################### Function #####################################################################
def generate_unique_id():
    return int(datetime.timestamp(datetime.now()) * 1000)


async def take_rate(db: Session, current_user: UserSchema.Read, rate_id: int, request: Request):
    account = await AccountController.get_by_user_id(db=db, user_id=current_user.id)
    await AccountController.subscribe_rate(db=db, rate_id=rate_id, account_id=account.id, request=request)
    return True


async def take_rate_by_id(db: Session, user_id: int, rate_id: int, request: Request):
    account = await AccountController.get_by_user_id(db=db, user_id=user_id)
    await AccountController.subscribe_rate(db=db, rate_id=rate_id, account_id=account.id, request=request)
    return True
