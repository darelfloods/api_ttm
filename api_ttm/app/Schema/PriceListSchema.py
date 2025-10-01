from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    libelle: str
    credit: int


class Create(Base):
    pass


class Read(Base):
    id: int
    created_at: datetime | None = None
    updated_at: datetime | None = None
