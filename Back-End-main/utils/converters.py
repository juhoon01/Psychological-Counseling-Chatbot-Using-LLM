# utils/converters.py
from model.user import UserTable
from model.room import RoomTable
from model.chat import ChatTable

from schemas.user import User
from schemas.room import Room
from schemas.chat import Chat


def room_table_to_schema(room_table: RoomTable) -> Room:
    chats = [chat_table_to_schema(
        chat) for chat in room_table.chats] if room_table.chats else []
    return Room(
        id=room_table.id,
        user_id=room_table.user_id,
        created_at=room_table.created_at,
        name=room_table.name,
        chats=chats
    )


def user_table_to_schema(user_table: UserTable) -> User:
    rooms = [room_table_to_schema(
        room) for room in user_table.rooms] if user_table.rooms else []
    return User(
        id=user_table.id,
        email=user_table.email,
        password=user_table.password,
        name=user_table.name,
        photo_id=user_table.photoId,
        rooms=rooms
    )


def chat_table_to_schema(chat_table: ChatTable) -> Chat:
    return Chat(
        id=chat_table.id,
        room_id=chat_table.room_id,
        ask=chat_table.ask,
        answer=chat_table.answer,
        model=chat_table.model,
        timestamp=chat_table.timestamp
    )
