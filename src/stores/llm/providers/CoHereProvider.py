from ..LLMInterface import LLMInterface
from ..LLMEnums import CoHereEnums, DocumentTypeEnum
import cohere
import logging
from typing import Any, cast, Union, List

class CoHereProvider(LLMInterface):
    
    def __init__(self, api_key: str ,
                       default_input_max_characters: int=1000,
                       default_generation_max_output_tokens: int=1000,
                       default_generation_temperature: float=0.1):
        
        self.api_key = api_key
        
        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_temperature = default_generation_temperature
        
        self.generation_model_id = None
        
        self.embedding_model_id = None
        self.embedding_size = None
        
        self.client = cohere.Client(self.api_key)
        self.enums = CoHereEnums
        self.logger = logging.getLogger(__name__)
        
    def set_generation_model(self, model_id: str):
        self.generation_model_id = model_id 
        
    def set_embedding_model(self, model_id: str, embedding_size: int):
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size        
        
    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    
    def generate_text(self, prompt: str, chat_history: list[Any] = [], max_output_tokens: int | None = None,
                            temperature: float | None = None) -> Any:
        
        if not self.client:
            self.logger.error("Embedding model for CoHere was not set.")
            return None     
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set.")
            return None
        
        max_output_tokens = max_output_tokens if max_output_tokens is not None else self.default_generation_max_output_tokens
        temperature = temperature if temperature is not None else self.default_generation_temperature 
        
        response = self.client.chat(
            model = self.generation_model_id,
            chat_history = chat_history,
            message = self.process_text(prompt),
            temperature = temperature,
            max_tokens = max_output_tokens
        )
        
        if not response or not response.text:
            self.logger.error("Error while generating text with CoHere")
            return None
        
        return response.text
    
    def embed_text(self, text: Union[str, List[str]], document_type: str | None = None) -> Any:
        if not self.client:
            self.logger.error("Embedding model for CoHere was not set.")
            return None

        if not self.embedding_model_id:
            self.logger.error("Embedding model for CoHere was not set.")
            return None

        if isinstance(text, str):
            normalized_text = text.strip()
            if not normalized_text:
                self.logger.warning("Empty text provided for CoHere embedding.")
                return None
            text = [normalized_text]
        else:
            if not text or all((item is None or str(item).strip() == "") for item in text):
                self.logger.warning("Empty text batch provided for CoHere embedding.")
                return None
            text = [str(item).strip() for item in text if str(item).strip()]

        input_type = CoHereEnums.DOCUMENT.value
        if document_type == DocumentTypeEnum.QUERY.value:
            input_type = CoHereEnums.QUERY.value

        response = self.client.embed(
            model = self.embedding_model_id,
            texts = text,
            input_type = input_type,
            embedding_types = ['float'],
        )
        
        if not response or not response.embeddings:
            self.logger.error("Error while embedding text with CoHere")
            return None

        return cast(Any, response.embeddings).float[0]
    
        
    def construct_prompt(self, prompt: str, role: str) -> Any:
        return {
            "role": role,
            "text": self.process_text(prompt)
        }