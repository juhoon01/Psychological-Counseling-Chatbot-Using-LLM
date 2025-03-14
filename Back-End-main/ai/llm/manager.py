import threading
from typing import Dict, Any

from ai.llm.config import model_dict, ModelConfig, AvailableModel, allowed_available_models
from ai.llm.scheduler import ModelScheduler
from log import logger


class AiModelManager:
    """모델 로딩 및 관리를 담당하는 클래스"""

    def __init__(self):
        self.able_model_list = list(model_dict.keys())
        self.running_model_dict: Dict[str, Any] = {}
        self.model_locks: Dict[str, threading.Lock] = {
            model_name: threading.Lock() for model_name in self.able_model_list
        }
        self.scheduler = ModelScheduler()
        self._validate_models()

    def _validate_models(self):
        """열거형과 모델 딕셔너리의 일관성을 검증"""
        missing_models = [
            model for model in allowed_available_models if model not in model_dict
        ]
        if missing_models:
            error_msg = (
                f"Model enums (from ai.llm.config/available_model.py) {missing_models} "
                f"not found in model_dict (from ai/llm/config.py).\n"
                f"Models in enums: {allowed_available_models}\n"
                f"Models in model_dict: {list(model_dict.keys())}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        logger.info("모델 검증을 성공적으로 완료했습니다.")

    def load_llm_model(self, model: AvailableModel, **kwargs):
        """지정된 모델을 로드하고 반환합니다."""
        model_name = model.value
        if model_name not in self.running_model_dict:
            logger.info(f"모델 '{model_name}'을(를) 로드 중입니다.")
            lock = self.model_locks[model_name]
            with lock:
                if model_name not in self.running_model_dict:
                    config: ModelConfig = model_dict[model_name]
                    try:
                        model_instance = config.model_cls(
                            **{**config.args, **kwargs})
                        self.running_model_dict[model_name] = model_instance
                        self.scheduler.add_model(model_name, model_instance)
                        self.scheduler.start_processing()
                        logger.info(f"모델 '{model_name}'이(가) 성공적으로 로드되었습니다.")
                    except Exception as e:
                        logger.exception(
                            f"모델 '{model_name}' 로딩 중 오류가 발생했습니다: {e}")
                        raise
        else:
            logger.info(f"모델 '{model_name}'이(가) 이미 로드되어 있습니다.")
        return self.running_model_dict[model_name]

    def generate(self, model: AvailableModel, ask_query: str) -> str:
        """모델을 사용하여 응답을 생성합니다."""
        model_name = model.value
        if model_name not in self.running_model_dict:
            raise ValueError(f"모델 '{model_name}'이(가) 로드되지 않았습니다.")
        logger.info(f"모델 '{model_name}'을(를) 사용하여 응답을 생성합니다.")
        response = self.scheduler.generate(model_name, ask_query)
        logger.info(f"모델 '{model_name}'의 응답 생성이 완료되었습니다.")
        return response
