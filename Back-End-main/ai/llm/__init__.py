# ai/llm/__init__.py
from ai.llm.manager import AiModelManager
from ai.llm.config import AvailableModel

# ModelManager의 인스턴스를 생성합니다.
_ai_model_manager = AiModelManager()


def load_llm_model(model: AvailableModel, **kwargs):
    """
    지정된 모델을 로드하고 반환합니다.

    Args:
        model (AvailableModel): 로드할 모델.
        **kwargs: 모델 초기화 시 추가 인자.

    Returns:
        로드된 모델 인스턴스.
    """
    return _ai_model_manager.load_llm_model(model, **kwargs)


def generate_response(model: AvailableModel, ask_query: str) -> str:
    """
    지정된 모델을 사용하여 응답을 생성합니다.

    Args:
        model (AvailableModel): 응답을 생성할 모델.
        ask_query (str): 사용자 질문.

    Returns:
        str: 모델이 생성한 응답.
    """
    return _ai_model_manager.generate(model, ask_query)
