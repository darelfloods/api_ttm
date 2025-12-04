from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Double, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    category = Column(String)
    pharmacy = Column(String, nullable=False)
    cip = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False) 