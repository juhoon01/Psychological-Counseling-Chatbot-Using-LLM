# services/chat.py
from sqlalchemy.orm import Session, joinedload
from datetime import datetime
from typing import Optional

from schemas.chat import *
from ai.llm import load_llm_model, generate_response
from schemas.room import CreateRoomInput, Room
from model.chat import ChatTable
from model.room import RoomTable
from error.exceptions import ChatNotFoundError, UnauthorizedError
from utils.converters import chat_table_to_schema, room_table_to_schema
from services.room import room_service
from ai.llm.config import AvailableModel, str_to_available_model
from ai.rag import rag_service
from log import logger


class ChatService:
    def _get_user_room(self, db: Session, room_id: int, user_id: str) -> Optional[RoomTable]:
        return db.query(RoomTable).filter(
            RoomTable.id == room_id,
            RoomTable.user_id == user_id
        ).first()

    async def create_chat(self, db: Session, create_chat_input: CreateChatInput, user_id: str) -> Chat:
        if create_chat_input.room_id == None:
            room = room_service.create_room(db, CreateRoomInput(), user_id)
            create_chat_input.room_id = room.id
        else:
            room = self._get_user_room(db, create_chat_input.room_id, user_id)
            if room.user_id != user_id:
                raise UnauthorizedError(
                    "You are not authorized to create a chat for this room")

        print("ASK:", create_chat_input.ask)
        # rag_responses = rag_service.search_in_rag(create_chat_input.ask)
        # print("RAG RESPONSES:", rag_responses)
        # logger.info(f"RAG RESPONSES: {rag_responses}")
        # rag_prompt = create_chat_input.ask
        # for i in range(len(rag_responses)):
        #     rag_prompt += f"{i+1}. {rag_responses[i]}\n"

        if create_chat_input.model == None:
            create_chat_input.model = AvailableModel.MOCK.value
        use_model = str_to_available_model(create_chat_input.model)

        # LLM 모델 로드 및 응답 생성
        load_llm_model(use_model)  # 이미 모델이 로드 되어있으면 로드하지 않음.
        response = generate_response(use_model, create_chat_input.ask)
        print("RESPONSE: ", response)

        create_chat_data = create_chat_input.model_dump()
        create_chat_data['answer'] = response
        create_chat_data['timestamp'] = datetime.now()

        chat_table = ChatTable(**create_chat_data)
        db.add(chat_table)
        db.commit()
        db.refresh(chat_table)

        return chat_table_to_schema(chat_table)

    def get_chat_by_id(self, db: Session, chat_id: int, user_id: str) -> Chat:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise ChatNotFoundError(f"Chat with id {chat_id} not found")
        return chat_table_to_schema(chat_table)

    def inspect_status(self, db: Session, room_id: int, user_id: str) -> Optional[str]:
        # 1. DB에서 chat_id에 해당하는 chats을 가져온다.
        room = db.query(RoomTable).options(joinedload(RoomTable.chats)).filter(
            RoomTable.id == room_id,
            RoomTable.user_id == user_id
        ).first()
        chats = room.chats
        if chats == None or len(chats) == 0:
            raise ChatNotFoundError(f"Room with id {room_id} not found")

        # 만약 채팅이 3개 미만일 경우 분석 거절
        if len(chats) < 3:
            return None

        # 2. 사용자의 질문들만 가져온다.
        # asks = [chat.ask for chat in chats]
        asks = ''
        for chat in chats:
            asks += chat.ask + '\n'

        asks = ''
        for i in range(len(chats)):
            asks += f"질문 {i+1}: {chats[i].ask}\n"
        logger.info(f"ASKS: {asks}")

        # 모델을 불러온다.
        use_model_name = "MentalLlm"
        use_model = str_to_available_model(use_model_name)
        load_llm_model(use_model)  # 이미 모델이 로드 되어있으면 로드하지 않음.

        # 질문 요약
        asks_prompt = f"사용자의 경험과 고유의 단어를 포함하여 위 대화를 구체적으로 요약하여라.\n{asks}"
        asks_short_res = generate_response(use_model, asks_prompt)
        logger.info(f"ASKS SHORT RES: {asks_short_res}")

        # RAG 검색
        rag_responses = rag_service.search_in_rag(asks_short_res)
        rag_result_str = ""
        for i in range(len(rag_responses)):
            rag_result_str += f"질문 {i+1}: {rag_responses[i].metadata['질문']}\n" 
            rag_result_str += f"사용자 증상 {i+1}: {rag_responses[i].metadata['사용자 증상']}\n"
            rag_result_str += f"의사진단 {i+1}: {rag_responses[i].metadata['의사진단']}\n"
            rag_result_str += f"진단 근거 {i+1}: {rag_responses[i].metadata['진단 근거']}\n"
            rag_result_str += f"해결책 {i+1}: {rag_responses[i].metadata['해결책']}\n\n"
        logger.info(f"RAG RESPONSES: {rag_result_str}")

        # 답변 생성
        # rag_prompt = "{ask_short_res}\n위 대화는 사용자의 상담내용을 요약한 것이다. 심리상담 전문가가 되어 다음의 사용자의 사용자의 질문과 유사한 질문에 대한 문답 데이터 쌍에 기반하여 답변하여라.\n{rag_result_str}"
        rag_prompt = "{rag_result_str} 위 내용에 기반하여 사용자의 질문에 대한 답변을 작성하여라.\n사용자의 질문: {asks_short_res}"
        response = generate_response(use_model, rag_prompt)
        logger.info(f"RESPONSE: {response}")

        return response

    def get_all_chats_by_room(self, db: Session, room_id: str, user_id: str) -> Room:
        room = db.query(RoomTable).options(joinedload(RoomTable.chats)).filter(
            RoomTable.id == room_id,
            RoomTable.user_id == user_id
        ).first()

        if not room:
            raise UnauthorizedError(
                "You are not authorized to view chats for this room")

        return room_table_to_schema(room)

    def update_chat(self, db: Session, chat_id: int, update_chat_input: UpdateChatInput, user_id: str) -> Chat:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise UnauthorizedError(
                "You are not authorized to view chats for this room")

        # LLM 모델 로드 및 응답 생성
        use_model = str_to_available_model(update_chat_input.model)
        load_llm_model(use_model)
        response = generate_response(use_model, update_chat_input.ask)

        update_chat_data = update_chat_input.model_dump()
        update_chat_data['answer'] = response
        update_chat_data['timestamp'] = datetime.now()
        update_chat_data['room_id'] = chat_table.room_id

        chat_table.update(**update_chat_data)
        db.commit()
        db.refresh(chat_table)

        return chat_table_to_schema(chat_table)

    def delete_chat(self, db: Session, chat_id: int, user_id: str) -> None:
        chat_table = db.query(ChatTable).join(RoomTable).filter(
            ChatTable.id == chat_id,
            RoomTable.user_id == user_id
        ).first()
        if not chat_table:
            raise ChatNotFoundError(f"Chat with id {chat_id} not found")

        db.delete(chat_table)
        db.commit()


chat_service = ChatService()
