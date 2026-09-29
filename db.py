from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker, declarative_base


# SQLite database URL
DATABASE_URL = "sqlite:///./doctor_patient.db"


# Create database engine
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)


# Enable SQLite foreign key constraints
@event.listens_for(engine, "connect")
def enable_foreign_keys(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


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