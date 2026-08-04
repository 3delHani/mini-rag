from abc import ABC, abstractmethod
from typing import Any

class LLMInterface(ABC):
    
    @abstractmethod
    def set_generation_model(self, model_id: str):
        pass
    
    @abstractmethod
    def set_embedding_model(self, model_id: str, embedding_size: int):
        pass
    
    @abstractmethod
    def generate_text(self, prompt: str, chat_history: list[Any] = [], max_output_tokens: int | None = None,
                            temperature: float | None = None) -> Any:
        pass
    
    @abstractmethod
    def embed_text(self, text: str, document_type: str | None = None) -> Any:
        pass
    
    @abstractmethod
    def construct_prompt(self, prompt: str, role: str):
        pass