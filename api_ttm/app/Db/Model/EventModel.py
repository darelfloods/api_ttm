from sqlalchemy import Column, Integer, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    ip_address = Column(String)
    action = Column(String)
    entity = Column(String)
    entity_id = Column(String)
    current_user_id = Column(Integer)
    amount = Column(Double)
    date_time = Column(DateTime, default=func.now(), nullable=False)
