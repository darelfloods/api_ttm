from pydantic import BaseModel
from datetime import datetime

from . import UserSchema, RateSchema, AccountSchema, PriceListSchema


class Base(BaseModel):
    ip_address: str | None = None
    action: str | None = None
    entity: str | None = None
    entity_id: str | None = None
    amount: float | None = None
    current_user_id: int | None = None


class Create(Base):
    pass


class Read(Base):
    date_time: datetime | None = None
