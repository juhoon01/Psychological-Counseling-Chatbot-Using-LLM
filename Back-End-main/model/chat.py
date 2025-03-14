from __future__ import annotations
from sqlalchemy import Column, String, ForeignKey, DateTime, Text, Integer
from sqlalchemy.orm import relationship
from db_base import DB_Base
from datetime import datetime


class ChatTable(DB_Base):
    __tablename__ = 'chat'

    id = Column(Integer, primary_key=True, unique=True,
                nullable=False, autoincrement=True)
    room_id = Column(String, ForeignKey('room.id'), nullable=False)
    ask = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    model = Column(String, nullable=False)
    timestamp = Column(
        DateTime, default=datetime.now, nullable=False)

    # 채팅방과의 관계 설정
    room = relationship("RoomTable", back_populates="chats")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @classmethod
    def create(cls, data: dict) -> ChatTable:
        return cls(**data)

    def __repr__(self):
        return f"<Chat(id={self.id}, room_id={self.room_id}, ask={self.ask}, answer={self.answer}, model={self.model}, timestamp={self.timestamp})>"

    def to_dict(self):
        return {
            'id': self.id,
            'room_id': self.room_id,
            'ask': self.ask,
            'answer': self.answer,
            'model': self.model,
            'timestamp': self.timestamp.isoformat()
        }

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        return self
