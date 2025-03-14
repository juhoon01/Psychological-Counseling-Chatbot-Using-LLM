# apis/room.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from services.room import room_service
from schemas.room import *
from db import get_db_session
from error.handler import handle_http_exceptions

router = APIRouter(
    prefix="/room",
    tags=["room"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateRoomOutput)
@handle_http_exceptions
def create_room_endpoint(
        create_room_input: CreateRoomInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreateRoomOutput:
    room = room_service.create_room(db, create_room_input, user_id)
    return CreateRoomOutput(room=room, success=True, message="Room created successfully")


@router.get("/myrooms", dependencies=[Depends(JWTBearer())], response_model=GetUserRoomsOutput)
@handle_http_exceptions
def get_user_rooms_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetUserRoomsOutput:
    rooms = room_service.get_all_rooms_by_user(db, user_id)
    return GetUserRoomsOutput(rooms=rooms, success=True, message="Rooms fetched successfully")


@router.get("/{room_id}", dependencies=[Depends(JWTBearer())], response_model=GetRoomOutput)
@handle_http_exceptions
def get_room_endpoint(
        room_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetRoomOutput:
    room = room_service.get_room_by_id(db, room_id, user_id)
    return GetRoomOutput(room=room, success=True, message="Room fetched successfully")


@router.put("/{room_id}", dependencies=[Depends(JWTBearer())], response_model=UpdateRoomOutput)
@handle_http_exceptions
def update_room_endpoint(
        room_id: int,
        update_room_input: UpdateRoomInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateRoomOutput:
    room = room_service.update_room(
        db, room_id, update_room_input, user_id)
    return UpdateRoomOutput(room=room, success=True, message="Room updated successfully")


@router.delete("/{room_id}", dependencies=[Depends(JWTBearer())], response_model=DeleteRoomOutput)
@handle_http_exceptions
def delete_room_endpoint(
        room_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteRoomOutput:
    room_service.delete_room(db, room_id, user_id)
    return DeleteRoomOutput(success=True, message="Room deleted successfully")
