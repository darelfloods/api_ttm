from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Base(BaseModel):
    libelle: str
    price: float
    credit: int


class Create(Base):
    image_url: Optional[str] = None
    badge_icon: Optional[str] = None
    badge_text: Optional[str] = None
    is_popular: Optional[bool] = False
    display_order: Optional[int] = 0
    is_active: Optional[bool] = True


class Read(Base):
    id: int
    image_url: Optional[str] = None
    badge_icon: Optional[str] = None
    badge_text: Optional[str] = None
    is_popular: Optional[bool] = False
    display_order: Optional[int] = 0
    is_active: Optional[bool] = True
    created_at: datetime | None = None
    updated_at: datetime | None = None


class Schema(Read):
    class Config:
        from_attributes = True
