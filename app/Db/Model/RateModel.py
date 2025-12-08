from sqlalchemy import Column, Integer, BigInteger, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    libelle = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    credit = Column(BigInteger, nullable=False)  # BigInteger pour supporter de très grandes valeurs
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    account = relationship("Account", back_populates="rate")
