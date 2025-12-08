from sqlalchemy import Column, Integer, BigInteger, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    libelle = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    credit = Column(BigInteger, nullable=False)  # BigInteger pour supporter de très grandes valeurs
    image_url = Column(String, nullable=True)  # URL de l'image de l'offre
    badge_icon = Column(String, nullable=True)  # Icône du badge (ex: 'fas fa-crown')
    badge_text = Column(String, nullable=True)  # Texte du badge (ex: 'VIP', 'Populaire')
    is_popular = Column(Boolean, default=False, nullable=False)  # Marquer comme populaire
    display_order = Column(Integer, default=0, nullable=False)  # Ordre d'affichage
    is_active = Column(Boolean, default=True, nullable=False)  # Activer/désactiver l'offre
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    account = relationship("Account", back_populates="rate")
