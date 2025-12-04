from pydantic import BaseModel
from datetime import datetime

from . import UserSchema
from . import RateSchema


class Base(BaseModel):
    credit: int
    subscription_date: datetime | None = None
    activate: bool | None = None
    user_id: int
    rate_id: int | None = None


class Create(Base):
    pass


class Read(Base):
    id: int
    created_at: datetime
    updated_at: datetime


class Schema(Read):
    user: UserSchema.Read
    rate: RateSchema.Read | None = None

    class Config:
        from_attributes = True
