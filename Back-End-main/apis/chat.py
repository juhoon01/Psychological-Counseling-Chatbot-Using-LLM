# apis/chat.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from services.chat import chat_service
from schemas.chat import *
from schemas.room import GetRoomChatsOutput
from db import get_db_session
from error.handler import handle_http_exceptions
from time import sleep

router = APIRouter(
    prefix="/chat",
    tags=["chat"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", dependencies=[Depends(JWTBearer())], response_model=CreateChatOutput)
@handle_http_exceptions
async def create_chat_endpoint(
        create_chat_input: CreateChatInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> CreateChatOutput:
    chat = await chat_service.create_chat(db, create_chat_input, user_id)
    return CreateChatOutput(chat=chat, success=True, message="Chat created successfully")


@router.get("/chat/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=GetChatOutput)
@handle_http_exceptions
def get_chat_endpoint(
        chat_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetChatOutput:
    chat = chat_service.get_chat_by_id(db, chat_id, user_id)
    return GetChatOutput(chat=chat, success=True, message="Chat fetched successfully")


@router.get("/room/{room_id}", dependencies=[Depends(JWTBearer())], response_model=GetRoomChatsOutput)
@handle_http_exceptions
def get_room_chats_endpoint(
        room_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetRoomChatsOutput:
    room = chat_service.get_all_chats_by_room(db, room_id, user_id)
    return GetRoomChatsOutput(room=room, success=True, message="Chats fetched successfully")


@router.put("/update/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=UpdateChatOutput)
@handle_http_exceptions
def update_chat_endpoint(
        chat_id: int,
        update_chat_input: UpdateChatInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateChatOutput:
    chat = chat_service.update_chat(
        db, chat_id, update_chat_input, user_id)
    return UpdateChatOutput(chat=chat, success=True, message="Chat updated successfully")


@router.delete("/delete/{chat_id}", dependencies=[Depends(JWTBearer())], response_model=DeleteChatOutput)
@handle_http_exceptions
def delete_chat_endpoint(
        chat_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteChatOutput:
    chat_service.delete_chat(db, chat_id, user_id)
    return DeleteChatOutput(success=True, message="Chat deleted successfully")


@router.get("/inspect/{room_id}", dependencies=[Depends(JWTBearer())], response_model=GetRoomInspectOutput)
@handle_http_exceptions
def get_room_chats_endpoint(
        room_id: int,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetRoomInspectOutput:
    status = chat_service.inspect_status(db, room_id, user_id)
#     status = """PTSD(외상 후 스트레스 장애)는 과거의 충격적인 사건이 현재의 삶에 지속적인 영향을 미치는 심리적 상태로, 많은 사람들이 겪는 문제입니다. 당신의 채팅 내용을 분석한 결과, 이와 유사한 증상이 보입니다. 이는 당신이 겪은 특정 사건이 감정, 사고, 그리고 행동에 큰 영향을 미치고 있다는 것을 보여줍니다. 하지만 중요한 사실은 PTSD는 극복할 수 있는 병이라는 것입니다. 적절한 도움과 노력으로 삶의 질을 회복하고 더욱 건강한 마음을 가질 수 있습니다.
# PTSD를 극복하기 위해 가장 중요한 것은 전문가의 도움을 받는 것입니다. 심리치료, 특히 인지행동치료(CBT)나 노출치료는 증상을 완화하고, 고통스러운 기억을 건강하게 다루는 데 효과적입니다. 또한 필요하다면 약물 치료를 병행하여 증상을 안정화할 수도 있습니다. 이와 더불어 일상 속에서 규칙적인 운동, 건강한 식단, 충분한 수면, 그리고 신뢰할 수 있는 사람들과의 소통을 통해 스스로를 돌보는 노력이 필요합니다. 특히, 자신의 감정을 억누르지 말고 이를 표현하는 연습을 하거나 일기를 쓰는 것도 큰 도움이 될 수 있습니다."""
    
    return GetRoomInspectOutput(success=True, message="Chats fetched successfully", status=status) if status != None else GetRoomInspectOutput(success=False, message="Chats fetched Failed")