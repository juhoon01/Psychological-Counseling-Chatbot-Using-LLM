import os
from dotenv import load_dotenv
from typing import Optional

from constants.path import PROJECT_DIR


class Env():
    def __init__(self):
        load_dotenv(os.path.join(PROJECT_DIR, ".env"))

    def get(self, key: str) -> Optional[str]:
        return os.environ.get(key)

    def set(self, key: str, value: str) -> None:
        os.environ[key] = value

    def unset(self, key: str) -> None:
        os.environ.pop(key)


env = Env()
