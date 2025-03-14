from bcrypt import hashpw, checkpw, gensalt
from typing import ClassVar


class AuthBcrypt:
    ENCODING: ClassVar[str] = 'utf-8'

    @staticmethod
    def hash_password(password: str) -> str:
        """
        주어진 비밀번호를 bcrypt를 사용하여 해싱함.

        :param password: 해싱할 비밀번호 문자열
        :return: 해싱된 비밀번호 문자열
        """
        try:
            hashed = hashpw(password.encode(AuthBcrypt.ENCODING), gensalt())
            return hashed.decode(AuthBcrypt.ENCODING)
        except Exception as e:
            raise ValueError("비밀번호 해싱에 실패했습니다.") from e

    @staticmethod
    def verify_password(password: str, hashed_password: str) -> bool:
        """
        주어진 비밀번호가 해싱된 비밀번호와 일치하는지 확인함.

        :param password: 확인할 비밀번호 문자열
        :param hashed_password: 비교할 해싱된 비밀번호 문자열
        :return: 일치 여부 (True 또는 False)
        """
        try:
            return checkpw(password.encode(AuthBcrypt.ENCODING), hashed_password.encode(AuthBcrypt.ENCODING))
        except Exception as e:
            return False
