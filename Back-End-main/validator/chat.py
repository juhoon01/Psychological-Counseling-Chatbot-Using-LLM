# validators/chat.py
from ai.llm.config import allowed_available_models
from error.exceptions import UnAvailableModelError


def validate_model(v):
    if v not in allowed_available_models:
        raise UnAvailableModelError(f"Model {v} is not available")
    return v
