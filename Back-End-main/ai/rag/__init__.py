from typing import List
from langchain_openai import ChatOpenAI
from langchain.docstore.document import Document
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores.utils import DistanceStrategy
import pandas as pd
import os
from pydantic import BaseModel, field_validator


from constants.path import CSV_DATA_PATH, VECTOR_DB_PATH


class RagItem(BaseModel):
    id: int
    ask: str
    symptoms: str
    age_range: str
    doctor_assertion: str
    assertment: str
    base: str
    todo: str

    def get_from_list(self, data: List):
        self.id = data[0]
        self.symptoms = data[1]
        self.age_range = data[2]
        self.doctor_assertion = data[3]
        self.assertment = data[4]
        self.base = data[5]
        self.todo = data[6]

    def to_dict(self):
        return {
            'id': self.id,
            'symptoms': self.symptoms,
            'age_range': self.age_range,
            'doctor_assertion': self.doctor_assertion,
            'assertment': self.assertment,
            'base': self.base,
            'todo': self.todo
        }


class RagService():
    def __init__(self, top_k: int = 3):
        # SentenceTransformers 모델을 사용하여 임베딩 생성
        self.embedding_model = SentenceTransformerEmbeddings(
            model_name='all-mpnet-base-v2')

        if not os.path.exists(VECTOR_DB_PATH):
            vectorstore = self.create_vectordb()
        else:
            vectorstore = FAISS.load_local(
                VECTOR_DB_PATH, embeddings=self.embedding_model, allow_dangerous_deserialization=True)
        self.vectorstore = vectorstore

        self.retriever = vectorstore.as_retriever(
            search_type='mmr',
            search_kwargs={'k': top_k, 'lambda_mult': 0.9}
        )

    def create_vectordb(self):
        df = pd.read_csv(CSV_DATA_PATH)

        # Document 객체 생성 (메타데이터 포함)
        documents = [
            Document(
                page_content=row['질문'],
                metadata={
                    '질문': row['질문'],
                    '사용자 증상': row['사용자 증상'],
                    # '연령대': row['연령대'],
                    '의사진단': row['의사진단'],
                    '진단 근거': row['진단 근거'],
                    '해결책': row['해결책']}
            ) for _, row in df.iterrows()
        ]

        # FAISS 벡터 저장소 생성
        vectorstore = FAISS.from_documents(documents,
                                           embedding=self.embedding_model,
                                           distance_strategy=DistanceStrategy.COSINE)

        vectorstore.save_local(VECTOR_DB_PATH)
        return vectorstore

    def search_in_rag(self, query: str):
        results = self.retriever.get_relevant_documents(query)
        return results


rag_service = RagService()
