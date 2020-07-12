import os
import uuid

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import JSON, DateTime

PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@postgres:5432/jukebox")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "_user"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    profile = Column(JSON)
    email = Column(String(250))
    service_key = Column(String(250))
    service = Column(String(250))

    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    deleted_at = Column(DateTime)
