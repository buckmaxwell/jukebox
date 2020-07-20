import datetime
import os
import uuid

from sqlalchemy import Column, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import DateTime

PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@postgres:5432/jukebox")
Session = sessionmaker(bind=engine)
Base = declarative_base()

# TODO: this class definition is dry now but not for long
class Play(Base):
    __tablename__ = "plays"
    __table_args__ = {"schema": "player"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    isrc = Column(String(250))
    upc = Column(String(250))
    ean = Column(String(250))
    spotify_id = Column(String(250))
    room_code = Column(String(250))  # TODO: should this be id

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    deleted_at = Column(DateTime)
