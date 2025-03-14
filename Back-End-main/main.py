import uvicorn
from fastapi import FastAPI

from apis import router as main_router
from apis.user import router as user_router
from apis.room import router as room_router
from apis.chat import router as chat_router
from apis.raw import router as raw_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",  # 개발 환경
    "https://jaewone.github.io/k-project-react-chatapp",  # gh-pages 도메인
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 허용할 도메인 리스트
    allow_credentials=True,
    allow_methods=["*"],  # 허용할 HTTP 메서드 (GET, POST, 등)
    allow_headers=["*"],  # 허용할 HTTP 헤더
)

app.include_router(main_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(chat_router)
app.include_router(raw_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7701)
# uvicorn main:app --host 0.0.0.0 --port 8502 --reload
