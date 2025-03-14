from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from auth.auth_bearer import JWTBearer
from auth.auth_handler import signJWT
from services.user import user_service
from schemas.user import *
from db import get_db_session
from error.handler import handle_http_exceptions
from validator.access_code import check_access_code

router = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)


@router.post("/me", response_model=CreateUserOutput)
@handle_http_exceptions
def create_user_endpoint(
        create_user_input: CreateUserInput,
        db: Session = Depends(get_db_session)) -> CreateUserOutput:
    check_access_code(create_user_input.access_code)
    user = user_service.create_user(db, create_user_input)
    jwt_token = signJWT(user.id)
    return CreateUserOutput(user=user, token=jwt_token, success=True, message="User created successfully")


@router.get("/me", dependencies=[Depends(JWTBearer())], response_model=GetUserOutput)
@handle_http_exceptions
def get_current_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> GetUserOutput:
    user = user_service.get_user_by_id(db, user_id)
    return GetUserOutput(user=user, success=True, message="User fetched successfully")


@router.put("/me", dependencies=[Depends(JWTBearer())], response_model=UpdateUserOutput)
@handle_http_exceptions
def update_user_endpoint(
        update_user_input: UpdateUserInput,
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> UpdateUserOutput:
    user = user_service.update_user(db, user_id, update_user_input)
    return UpdateUserOutput(user=user, success=True, message="User updated successfully")


@router.post("/upload/profile", dependencies=[Depends(JWTBearer())])
async def upload_profile_image(
        file: UploadFile = File(...),
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> BaseOutput:
    success = user_service.upload_profile_photo(db, file, user_id)
    return BaseOutput(success=success, message="Profile image uploaded successfully" if success else "Profile image upload failed")


@router.delete("/me", dependencies=[Depends(JWTBearer())], response_model=DeleteUserOutput)
@handle_http_exceptions
def delete_user_endpoint(
        db: Session = Depends(get_db_session),
        user_id: str = Depends(JWTBearer())) -> DeleteUserOutput:
    user_service.delete_user(db, user_id)
    return DeleteUserOutput(success=True, message="User deleted successfully")


@router.post("/me/login", response_model=LoginUserOutput)
@handle_http_exceptions
def login(
        login_user_input: LoginUserInput,
        db: Session = Depends(get_db_session)) -> LoginUserOutput:
    user = user_service.login(db, login_user_input)
    jwt_token = signJWT(user.id)
    return LoginUserOutput(user=user, token=jwt_token, success=True, message="User logged in successfully")
