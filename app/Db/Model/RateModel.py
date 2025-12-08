from sqlalchemy import Column, Integer, BigInteger, String, func, DateTime, Boolean, ForeignKey, Double
from sqlalchemy.orm import relationship

from ..Connection import Base


class Rate(Base):
    __tablename__ = "rates"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    libelle = Column(String, nullable=False)
    price = Column(Double, nullable=False)
    credit = Column(BigInteger, nullable=False)  # BigInteger pour supporter de très grandes valeurs
    # Nouveaux champs optionnels pour la personnalisation des offres
    # Ces colonnes seront créées automatiquement lors du prochain déploiement
    image_url = Column(String, nullable=True, default=None)  # URL de l'image de l'offre
    badge_icon = Column(String, nullable=True, default=None)  # Icône du badge (ex: 'fas fa-crown')
    badge_text = Column(String, nullable=True, default=None)  # Texte du badge (ex: 'VIP', 'Populaire')
    is_popular = Column(Boolean, default=False, nullable=True)  # Marquer comme populaire
    display_order = Column(Integer, default=0, nullable=True)  # Ordre d'affichage
    is_active = Column(Boolean, default=True, nullable=True)  # Activer/désactiver l'offre
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), nullable=False)

    account = relationship("Account", back_populates="rate")
