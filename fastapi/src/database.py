from typing import Generator, Any
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.orm.decl_api import DeclarativeMeta
import os


# Base Model Class
Base: DeclarativeMeta = declarative_base()


class DbConnector:
    PG_DB = os.environ.get('SNEK_POSTGRES_DB')
    PG_USER = os.environ.get('SNEK_POSTGRES_USER')
    PG_PW = os.environ.get('SNEK_POSTGRES_PW')
    PG_HOST = os.environ.get('SNEK_POSTGRES_HOST')
    PG_URL: str = f"postgresql://{PG_USER}:{PG_PW}@{PG_HOST}:5432/{PG_DB}"

    engine: Engine = create_engine(PG_URL)
    SessionLocal: sessionmaker[Session] = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    @classmethod
    def get_db(cls) -> Generator[Session, Any, None]:
        db = cls.SessionLocal()
        try:
            yield db
        finally:
            db.close()
