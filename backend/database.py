import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import Session, sessionmaker

# Load database settings from the local .env file.
load_dotenv()

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = int(os.getenv("POSTGRES_PORT", "5432"))

if not all((POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD)):
    raise RuntimeError(
        "Missing database configuration. "
        "Check the required variables in your local .env file."
    )

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
    port=POSTGRES_PORT,
    database=POSTGRES_DB,
)

engine = create_engine(
    database_url,
    pool_pre_ping=True,
)

# Create a factory for database sessions.
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


# Provide one database session to a request and close it afterward.
def get_db():
    db: Session = SessionLocal()

    try:
        yield db
    finally:
        db.close()