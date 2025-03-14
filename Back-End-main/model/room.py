from __future__ import annotations
from sqlalchemy import Column, String, ForeignKey, DateTime, Integer
from sqlalchemy.orm import relationship
from db_base import DB_Base
from datetime import datetime


class RoomTable(DB_Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    user_id = Column(String, ForeignKey('user.id'), nullable=False)
    created_at = Column(
        DateTime, default=datetime.now, nullable=False)
    name = Column(String, nullable=True)

    # 사용자와의 관계 설정
    owner = relationship("UserTable", back_populates="rooms")

    # 채팅방 내 채팅들과의 관계 설정
    chats = relationship("ChatTable", back_populates="room",
                         cascade="all, delete-orphan", lazy='noload')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> RoomTable:
        return cls(**data)

    def __repr__(self):
        return f"<Room(id={self.id}, user_id={self.user_id}, created_at={self.created_at}, name={self.name})>"

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'name': self.name
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
