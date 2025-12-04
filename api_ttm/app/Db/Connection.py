from motor.motor_asyncio import AsyncIOMotorClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from core.config import settings

# Configuration de la connexion PostgreSQL
engine = create_engine(settings.DATABASE_URL)
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
