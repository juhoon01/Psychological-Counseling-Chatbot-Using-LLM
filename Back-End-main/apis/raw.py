# apis/room.py
from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from constants.path import PROFILE_PHOTO_DIR, ASSET_DIR
from utils.os_utils import get_image_path
from error.handler import handle_http_exceptions


router = APIRouter(
    prefix="/raw",
    tags=["raw"],
    responses={404: {"description": "Not found"}},
)


@router.get("/profile/{file_id}")
@handle_http_exceptions
async def read_file(file_id: str):
    file_path = get_image_path(file_id, PROFILE_PHOTO_DIR)
    return FileResponse(file_path if file_path != None else os.path.join(ASSET_DIR, 'default_profile_image.jpeg'))
