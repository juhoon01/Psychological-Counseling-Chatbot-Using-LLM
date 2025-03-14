# schemas/user.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

from schemas.common import BaseOutput
from schemas.room import Room


class User(BaseModel):
    id: str
    email: EmailStr
    password: str
    name: str
    photoId: Optional[str] = None
    rooms: Optional[List[Room]] = None

    class Config:
        from_attributes = True


class CreateUserInput(BaseModel):
    access_code: str
    email: EmailStr
    password: str
    name: str
    photoId: Optional[str] = None


class CreateUserOutput(BaseOutput):
    user: Optional[User] = None
    token: Optional[dict] = None


class GetUserOutput(BaseOutput):
    user: Optional[User] = None


class UpdateUserInput(BaseModel):
    id: str
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    name: Optional[str] = None


class UpdateUserOutput(BaseOutput):
    user: Optional[User] = None


class DeleteUserOutput(BaseOutput):
    pass


class LoginUserInput(BaseModel):
    email: EmailStr
    password: str


class LoginUserOutput(BaseOutput):
    user: Optional[User] = None
    token: Optional[dict] = None
