# schemas/common.py
from pydantic import BaseModel
from typing import Optional, List


class BaseOutput(BaseModel):
    success: bool
    message: str
