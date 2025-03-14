from dataclasses import dataclass
from typing import Type, Dict, Any
from enum import Enum

from error.exceptions import UnAvailableModelError
from ai.llm.models import MockModel, MentalLlm, AnalysingLlm


@dataclass
class ModelConfig:
    model_cls: Type
    args: Dict[str, Any]

class AvailableModel(str, Enum):
    """Available models"""
    MOCK = 'Mock'
    MentalLlm = 'MentalLlm'
    AnalysingLlm = 'AnalysingLlm'


model_dict = {
    AvailableModel.MOCK.value: ModelConfig(
        model_cls=MockModel,
        args={'model_name': "Mock", 'delay': 3, 'init_delay': 3}
    ),
    AvailableModel.MentalLlm.value: ModelConfig(
        model_cls=MentalLlm,
        args={'model_name': "MentalLlm", 'device': 'cuda'}
    ),
    AvailableModel.AnalysingLlm.value: ModelConfig(
        model_cls=AnalysingLlm,
        args={'model_name': "AnalysingLlm", 'device': 'cuda'}
    ),
    # AvailableModel.GEMMA.value: ModelConfig(
    #     model_cls=GemmaModel,
    #     args={'model_name': 'Gemma', 'max_length': 128}
    # ),
    # AvailableModel.LLAMA2.value: ModelConfig(
    #     model_cls=LLama2Model,
    #     args={'model_name': 'LLama2', 'max_length': 512, 'device': 'cuda'}
    # ),
}


allowed_available_models = tuple(e.value for e in AvailableModel)


def str_to_available_model(model: str) -> AvailableModel:
    if model in allowed_available_models:
        return AvailableModel(model)
    raise UnAvailableModelError(f"Model {model} is not available")
