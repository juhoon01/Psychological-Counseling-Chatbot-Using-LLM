from fastapi import APIRouter

router = APIRouter(
    prefix="",
    tags=[""],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def root():
    return {'Hello': '환영합니다! 2024년 2학기 K프로젝트의 최인엽 교수팀의 API 서버입니다.'}
