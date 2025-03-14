from time import sleep
import torch
import re
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

from ai.llm.models.interface.base_ai_model import BaseAiModel
from log import logger

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
from ai.llm.models.interface.base_ai_model import BaseAiModel
from log import logger

class MentalLlm(BaseAiModel):
    def __init__(self, max_length=512, model_name="MentalLlm", **kwags):
        self.max_length = max_length
        self.user_name = "사용자"
        self.device = kwags.get('device', 'cpu')

        # 모델과 토크나이저 로드
        load_model_name = "juhoon01/ko_llama3_model_shinhan_4"
        self.model = AutoModelForCausalLM.from_pretrained(load_model_name, torch_dtype=torch.float32)
        self.tokenizer = AutoTokenizer.from_pretrained(load_model_name)

        logger.info(f"Load {model_name} model complete.")

    def preProcess(self, text: str) -> str:
        """ LLM에 입력하기 전에 전처리를 수행"""
        return text

    def postProcess(self, text: str) -> str:
        """ LLM의 출력을 후처리"""
        text = (text.replace("사우", f"{self.user_name}")
                    .replace("용자님", f"{self.user_name}님")
                    .replace("용자", f"{self.user_name}")
                    .replace("사용자님", f"{self.user_name}님")
                    .replace("사용자", f"{self.user_name}")
                    .replace("사우님", f"{self.user_name}")
                    .replace("undefined", ""))
        text = re.sub(r'<\|.*?\|>', '', text)
        text = re.sub(r'\|endoftask\|=1>', '', text)

        # Remove text within angle brackets (e.g., <br>, <p>, </li>, etc.)
        text = re.sub(r'<[^<>]*>', '', text)

        # Remove incomplete tags or tokens starting with < or ending with >
        text = re.sub(r'<[^ ]*', '', text)
        text = re.sub(r'[^ ]*>', '', text)

        # Remove special characters that may have been left behind
        text = re.sub(r'[<>]', '', text)

        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def remove_repeated_sentences(self, text: str) -> str:
        return text
        """텍스트에서 반복되는 문장을 제거"""
        seen = set()
        result = []
        for sentence in text.split('. '):  # 문장을 '.' 기준으로 나눔
            sentence = sentence.strip()   # 공백 제거
            if sentence not in seen:
                seen.add(sentence)
                result.append(sentence)
        return '. '.join(result)

    def generate_response(self, prompt: str) -> str:
        """ 사용자 입력에 대한 응답 생성 """
        # 프롬프트만 사용
        full_prompt = f"### 질문: {prompt}\n### 답변:"
        inputs = self.tokenizer(full_prompt, return_tensors="pt", truncation=True).to(self.device)

        # 응답 생성
        outputs = self.model.generate(
            inputs.input_ids,
            max_new_tokens=150,  # 더 많은 텍스트를 생성
            temperature=0.7,
            top_p=0.85,
            top_k=50,
            repetition_penalty=2.5,
            no_repeat_ngram_size=3
        )

        # 생성된 텍스트 디코딩 및 후처리
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = response.replace("<|endoftext|>", "").strip()

        # 반복 제거 (필요시)
        response = self.postProcess(self.remove_repeated_sentences(response))

        # 필요 없는 텍스트 제거
        if "### 질문:" in response:
            response = response.split("### 질문:")[-1]  # 마지막 응답만 가져옴

        # ### 답변: 이후의 텍스트만 가져옴
        if "### 답변:" in response:
            response = response.split("### 답변:")[-1].strip()

        return response


    def set_max_length(self, max_length):
        self.max_length = max_length


mental_llm = MentalLlm(device='cuda')