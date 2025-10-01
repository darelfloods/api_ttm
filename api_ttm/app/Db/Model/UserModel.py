from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from ..Connection import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    firstname = Column(String)
    lastname = Column(String, nullable=False)
    email = Column(String, unique=True)
    phone = Column(String)
    role = Column(String)
    password = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    account = relationship("Account", back_populates="user")
