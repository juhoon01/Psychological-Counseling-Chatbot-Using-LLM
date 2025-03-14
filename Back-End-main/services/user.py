from sqlalchemy.orm import Session, joinedload
from typing import Optional
from fastapi import UploadFile
import os

from schemas.user import *
from model.user import UserTable
from auth.auth_bcrypt import AuthBcrypt
from error.exceptions import (
    UserNotFoundError, UnauthorizedError, DuplicateEmailError)
from utils.converters import user_table_to_schema
from constants.path import PROFILE_PHOTO_DIR
from utils.os_utils import save_image


class UserService:
    def _get_user_by_id(self, db: Session, user_id: str) -> Optional[UserTable]:
        return db.query(UserTable).filter(UserTable.id == user_id).first()

    def _get_user_by_email(self, db: Session, email: str) -> Optional[UserTable]:
        return db.query(UserTable).filter(UserTable.email == email).first()

    def _validate_unique_user(self, db: Session, email: str) -> None:
        if self._get_user_by_email(db, email):
            raise DuplicateEmailError("Email already exists")

    def _update_user(self, db: Session, user_table: UserTable, data: dict) -> UserTable:
        user_table.update(**data)
        db.commit()
        db.refresh(user_table)
        return user_table

    def create_user(self, db: Session, create_user_input: CreateUserInput) -> User:
        self._validate_unique_user(db, create_user_input.email)

        create_user_input.password = AuthBcrypt.hash_password(
            create_user_input.password)

        user_table = UserTable(
            **create_user_input.model_dump(exclude={"access_code"}))
        db.add(user_table)
        db.commit()
        db.refresh(user_table)

        return user_table_to_schema(user_table)

    def get_user_by_id(self, db: Session, user_id: str) -> User:
        user_table = db.query(UserTable).options(joinedload(UserTable.rooms)).filter(
            UserTable.id == user_id).first()
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")

        return user_table_to_schema(user_table)

    def update_user(self, db: Session, user_id: str, update_user_input: UpdateUserInput) -> User:
        user_table = self._get_user_by_id(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")

        if update_user_input.email:
            self._validate_unique_user(db, update_user_input.email)

        if update_user_input.password:
            update_user_input.password = AuthBcrypt.hash_password(
                update_user_input.password)

        user_table = self._update_user(
            db, user_table, update_user_input.model_dump(exclude_unset=True))

        return user_table_to_schema(user_table)

    def upload_profile_photo(self, db: Session, file: UploadFile, user_id: str):
        user_table = self._get_user_by_id(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")

        file_id = f"{user_id}.jpeg"
        file_path = os.path.join(PROFILE_PHOTO_DIR, file_id)
        save_image(file_path, file, save_format="JPEG")

        self._update_user(db, user_table, {"photoId": file_id})

        return True

    def delete_user(self, db: Session, user_id: str) -> None:
        user_table = self._get_user_by_id(db, user_id)
        if not user_table:
            raise UserNotFoundError(f"User with id {user_id} not found")

        db.delete(user_table)
        db.commit()

    def login(self, db: Session, login_user_input: LoginUserInput) -> User:
        user_table = self._get_user_by_email(db, login_user_input.email)
        if not user_table:
            raise UserNotFoundError(
                f"User with email {login_user_input.email} not found")

        if not AuthBcrypt.verify_password(login_user_input.password, user_table.password):
            raise UnauthorizedError("Unauthorized user password")

        return user_table_to_schema(user_table)


user_service = UserService()
