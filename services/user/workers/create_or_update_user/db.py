from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import DateTime
from sqlalchemy.types import JSON
import os

PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@postgres:5432/jukebox")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "_user"}

    id = Column(Integer, primary_key=True)

    profile = Column(JSON)
    email = Column(String(250))
    service_key = Column(String(250))
    service = Column(String(250))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
