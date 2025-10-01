from pydantic import BaseModel
from typing import Any
from datetime import datetime


class Base(BaseModel):
    name: str
    description: str | None = None
    price: float
    stock: int
    category: str | None = None
    pharmacy: str
    cip: str


class Create(Base):
    pass


class Read(Base):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Reservation(BaseModel):
    pharmacy: str | None = None
    buyer: str | None = None
    buyerPhone: str | None = None
    buyerEmail: str | None = None
    produits: Any | None = None
