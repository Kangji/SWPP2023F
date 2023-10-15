from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
import os


PG_DB = os.environ.get('SNEK_POSTGRES_DB')
PG_USER = os.environ.get('SNEK_POSTGRES_USER')
PG_PW = os.environ.get('SNEK_POSTGRES_PW')
TEST_DB_URL: str = f"postgresql://{PG_USER}:{PG_PW}@localhost:5432/{PG_DB}"


engine: Engine = create_engine(TEST_DB_URL)
SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base Model Class
Base: DeclarativeMeta = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
