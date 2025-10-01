from pydantic import BaseModel
from datetime import datetime


class Base(BaseModel):
    firstname: str | None = None
    lastname: str | None = None
    email: str | None = None
    phone: str | None = None
    role: str | None = None


class Create(Base):
    password: str


class Read(Base):
    id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Schema(Read):
    class Config:
        from_attributes = True
