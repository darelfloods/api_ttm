from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

from core.config import settings

# Configuration de la connexion PostgreSQL avec pool optimisé pour Render
engine = create_engine(
    settings.DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,                    # Nombre de connexions permanentes
    max_overflow=10,                # Connexions supplémentaires en cas de pic
    pool_pre_ping=True,             # Vérifie que la connexion est vivante avant utilisation
    pool_recycle=3600,              # Recycle les connexions après 1h (évite les timeouts)
    connect_args={
        "connect_timeout": 10,      # Timeout de connexion à 10s
        "options": "-c statement_timeout=30000"  # Timeout des requêtes à 30s
    }
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configuration de la connexion MongoDB
MONGODB_URL = settings.MONGODB_URL
client = AsyncIOMotorClient(MONGODB_URL)
db = client[settings.MONGODB_DB_NAME]

# Collection pour les produits
products_collection = db.products
