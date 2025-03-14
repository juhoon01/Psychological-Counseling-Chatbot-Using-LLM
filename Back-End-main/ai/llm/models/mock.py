from time import sleep

from ai.llm.models.interface.base_ai_model import BaseAiModel
from log import logger


class MockModel(BaseAiModel):
    def __init__(self, max_length=30, delay=3, init_delay=2, model_name="MockModel", **kwags):
        self.max_length = max_length
        self.delay = delay
        sleep(init_delay)
        logger.info(f"Load {model_name} model complete.")

    def generate_response(self, prompt, messages=[]):
        sleep(self.delay)
        return f"Mock response to {prompt}"

    def preProcess(self, text: str) -> str:
        """ LLM에 입력하기 전에 전처리를 수행"""
        return text

    def postProcess(self, text: str) -> str:
        """ LLM의 출력을 후처리"""
        return text

    def set_max_length(self, max_length):
        self.max_length = max_length
