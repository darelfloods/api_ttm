from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    libelle: str
    price: float
    credit: int


class Create(Base):
    pass


class Read(Base):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Schema(Read):
    class Config:
        from_attributes = True
