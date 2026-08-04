from ..LLMInterface import LLMInterface
from ..LLMEnums import OllamaEnums

import requests
import logging
from typing import List, Union, Any 


class Ollama(LLMInterface):

    def __init__(self,
                 api_key: str, 
                 base_url: str = "http://localhost:11434",
                 default_input_max_characters: int = 1024,
                 default_generation_output_max_tokens: int = 1024,
                 default_generation_temperature: float = 0.1):
        

        self.base_url = base_url.rstrip("/")
        self.enums = OllamaEnums
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_output_max_tokens = default_generation_output_max_tokens
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.logger = logging.getLogger(__name__)
        
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id 
        
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size        
    
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()

    def generate_text(self,
                      prompt: str,
                      chat_history: list[Any] | None = None,
                      max_output_tokens: int | None = None,
                      temperature: float | None = None) -> Any:
        
        if not self.generation_model_id:
            self.logger.error("Generation model ID is not set for Ollama.")
            return None

        history = (chat_history or [])[:]
        history = history + [self.construct_prompt(prompt, role=OllamaEnums.USER.value)]

        payload: dict[str, Any] = {
            "model": self.generation_model_id,
            "messages": history,
            "options": {
                "temperature": temperature or 0.1, 
                "num_predict": max_output_tokens or self.default_generation_output_max_tokens
                },
            "stream": False
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json=payload
            )
            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Ollama generation request failed: {e}")
            return None
        
        result = response.json()
        return result.get("message", {}).get("content", "").strip()


    def embed_text(self, text: Union[str, List[str]], document_type: str | None = None):
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model ID is not set for Ollama.")
            return None
        
        # Ensure we always send a list of strings to Ollama
        if isinstance(text, str):
            inputs = [text]
        else:
            inputs = list(text)

        payload: dict[str, Any] = {
            "model": self.embedding_model_id,
            "input": inputs
        }

        try:
            response = requests.post(
                f"{self.base_url}/api/embed",
                json=payload
            )

            response.raise_for_status()
        except Exception as e:
            self.logger.error(f"Ollama embedding request failed: {e}")
            return None

        result = response.json()
        return result.get("embeddings") or None


    def construct_prompt(self, prompt: str, role: str) -> Any:
        return {"role": role, "content": prompt}
