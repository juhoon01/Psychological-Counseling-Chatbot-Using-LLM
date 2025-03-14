from core.env import env
from error.exceptions import WrongAccessCodeException


def check_access_code(access_code: str) -> bool:
    access_code_real = env.get("ACCESS_CODE")
    is_correct = access_code_real == access_code
    if not is_correct:
        raise WrongAccessCodeException("Access code is wrong")
