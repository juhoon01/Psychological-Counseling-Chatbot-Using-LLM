from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig, pipeline
from time import sleep
import torch

from ai.llm.models.interface.base_ai_model import BaseAiModel
from log import logger

class AnalysingLlm(BaseAiModel):
    def __init__(self, max_length=1024, model_name="AnalysingLlm", **kwargs):
        self.max_length = max_length
        self.user_name = "사용자"
        self.device = kwargs.get('device', 'cuda' if torch.cuda.is_available() else 'cpu')

        # Set quantization configuration
        quant_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=False,
        )

        # 모델과 토크나이저 로드
        model_save_path = "/home/billy/koalpaca/merged_psychopathy_model"
        base_model_name = "beomi/Llama-3-Open-Ko-8B"

        # Load the tokenizer from the base model (since it wasn't modified)
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_name,
            trust_remote_code=True
        )

        # Ensure tokenizer settings match the model
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

        # Load the fine-tuned model
        self.model = AutoModelForCausalLM.from_pretrained(
            model_save_path,
            device_map="auto",
            torch_dtype=torch.float16,
            quantization_config=quant_config,
            trust_remote_code=True,
        )

        logger.info(f"Load {model_name} model complete.")

    def preProcess(self, text: str) -> str:
        """ LLM에 입력하기 전에 전처리를 수행"""
        return text

    def postProcess(self, text: str) -> str:
        """ LLM의 출력을 후처리"""
        text = text.replace("사우", f"{self.user_name}")

        if "### 답변:" in text:
            answer = text.split("### 답변:")[1].strip()
        else:
            answer = text
        return text


    def generate_response(self, prompt: str, messages=[]):
        """
        prompt(str): 사용자의 입력
            - EX: prompt = "요즘 무기력하고 힘들어요. 에너지가 없어서 아무것도 하기 싫은 기분이 많이 들어요"
        messages(list): 사용자와의 이전 대화 내용
        """
        # LLM에 입력하기 전에 전처리를 수행
        prompt = self.preProcess(prompt)

        # Construct the input text
        input_text = f"의료 상담 전문가가 되어 다음 질문에 답하여라. 문장은 습니다, 합니다, 등의 공손한 말투를 사용하여라.\n### 질문: {prompt}\n### 답변:"

        # Tokenize the input text
        inputs = self.tokenizer(input_text, return_tensors="pt").to(self.device)

        # Generate the output tokens
        output_tokens = self.model.generate(
            inputs.input_ids,
            max_new_tokens=150,  # 더 많은 텍스트를 생성
            temperature=0.7,
            top_p=0.85,
            top_k=50,
            repetition_penalty=2.5,
            no_repeat_ngram_size=3,
        )

        # Decode the output tokens
        result = self.tokenizer.decode(output_tokens[0], skip_special_tokens=True)

        return self.postProcess(result)

    def set_max_length(self, max_length):
        self.max_length = max_length


# analysing_llm = AnalysingLlm(device='cuda')