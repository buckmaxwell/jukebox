from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import DateTime
from time import sleep
import os

PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@postgres:5432/jukebox")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Authorization(Base):
    __tablename__ = "authorizations"
    __table_args__ = {"schema": "authorizer"}

    id = Column(Integer, primary_key=True)

    access_token_expiration = Column(DateTime)
    access_token = Column(String(250))
    refresh_token = Column(String(250))
    scope = Column(String(250))
    service = Column(String(250))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
