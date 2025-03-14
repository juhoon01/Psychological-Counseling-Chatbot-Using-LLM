# db/__init__.py
import os
from log import logger
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker

# from core.env import env
from constants.path import PROJECT_DIR
from db_base import DB_Base
from model import *


# 2. 데이터베이스 URL 설정 using absolute path
DB_PATH = os.path.join(PROJECT_DIR, "Database.db")
DB_URL = f'sqlite:///{DB_PATH}'

engine = create_engine(DB_URL, connect_args={
                       "check_same_thread": False}, echo=False)


@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


# 4. 테이블 생성
try:
    DB_Base.metadata.create_all(engine)
    logger.info("테이블 생성 성공")
    logger.info(f"Database path: {DB_PATH}")
except Exception as e:
    logger.error(f"테이블 생성 실패: {e}")

# 5. 세션 생성기 설정
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 6. 의존성으로 사용할 세션 생성 함수


def get_db_session():
    """
    Dependency
    try-finally 블록을 통해 db 연결을 종료하거나 문제가 생겼을 때 무조건 close 해준다.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
