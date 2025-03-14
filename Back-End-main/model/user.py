# model/user.py
from __future__ import annotations
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import uuid

from db_base import DB_Base


class UserTable(DB_Base):
    __tablename__ = 'user'
    id = Column(String, primary_key=True, unique=True,
                nullable=False, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    name = Column(String, nullable=False)
    photoId = Column(String, nullable=True)

    # Relationship to RoomTable
    rooms = relationship("RoomTable", back_populates="owner",
                         cascade="all, delete-orphan", lazy='noload')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> UserTable:
        return cls(**data)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, password={self.password}, name={self.name}, photoId={self.photoId})>"

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'photoId': self.photoId
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
