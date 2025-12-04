from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    credit = Column(Integer, nullable=False, default=0)
    subscription_date = Column(DateTime)
    activate = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="account")
    rate_id = Column(Integer, ForeignKey("rates.id"))
    rate = relationship("Rate", back_populates="account")
