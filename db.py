from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite database URL
DATABASE_URL = "sqlite:///./doctor_patient.db"


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Create database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for SQLAlchemy models
Base = declarative_base()


# Database session dependency
def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=engine)