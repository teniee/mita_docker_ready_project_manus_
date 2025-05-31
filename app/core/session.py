from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings=get_settings()
engine=create_engine(settings.DATABASE_URL, echo=False, pool_pre_ping=True)
SessionLocal=sessionmaker(bind=engine, autocommit=False, autoflush=False)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()