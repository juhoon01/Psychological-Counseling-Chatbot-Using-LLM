# schemas/room.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from schemas.chat import Chat
from schemas.common import BaseOutput


class Room(BaseModel):
    id: int
    user_id: str
    created_at: datetime
    name: Optional[str] = None
    chats: Optional[List['Chat']] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class CreateRoomInput(BaseModel):
    name: Optional[str] = None


class CreateRoomOutput(BaseOutput):
    room: Optional[Room] = None


class GetRoomOutput(BaseOutput):
    room: Optional[Room] = None


class GetUserRoomsOutput(BaseOutput):
    rooms: Optional[List[Room]] = None


class UpdateRoomInput(BaseModel):
    name: Optional[str] = None


class UpdateRoomOutput(BaseOutput):
    id: int
    room: Optional[Room] = None


class DeleteRoomOutput(BaseOutput):
    pass  # No additional fields needed


# chat service schemas
class GetRoomChatsOutput(BaseOutput):
    room: Optional[Room] = None
