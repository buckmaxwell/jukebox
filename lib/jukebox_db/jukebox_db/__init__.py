#!/usr/bin/env/python3

import datetime
import os
import uuid

from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.types import JSON, DateTime

PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
engine = create_engine(f"postgresql://{PG_USER}:{PG_PASS}@postgres:5432/jukebox")
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = {"schema": "room"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    host = Column(String(250))
    code = Column(String(250))
    expiration = Column(DateTime)

    followers = relationship("Follower")

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    deleted_at = Column(DateTime)


class Follower(Base):
    __tablename__ = "followers"
    __table_args__ = {"schema": "room"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    room_id = Column(UUID, ForeignKey("room.rooms.id"))
    user_id = Column(UUID)

    room = relationship("Room", back_populates="followers")

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    deleted_at = Column(DateTime)


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


class Authorization(Base):
    __tablename__ = "authorizations"
    __table_args__ = {"schema": "authorizer"}

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )

    access_token_expiration = Column(DateTime)
    access_token = Column(String(250))
    refresh_token = Column(String(250))
    scope = Column(String(250))
    service = Column(String(250))

    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(
        DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now
    )
    deleted_at = Column(DateTime)


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


__version__ = "0.0.1"
