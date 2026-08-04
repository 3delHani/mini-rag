from .LLMEnums import LLMEnums
from .providers.OpenAIProvider import OpenAIProvider
from .providers.CoHereProvider import CoHereProvider
from .providers.VoyageProvider import VoyageProvider
from typing import Any

class LLMProviderFactory:
    def __init__(self, config: Any):
        self.config = config
    
    def create(self, provider : str) -> Any:
        if provider == LLMEnums.OPENAI.value:
            return OpenAIProvider(
                api_key = self.config.OPENAI_API_KEY,
                api_url = self.config.OPENAI_API_URL,
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )
            
        elif provider == LLMEnums.COHERE.value:
            return CoHereProvider(
                api_key = self.config.COHERE_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )
            
        elif provider == LLMEnums.VOYAGE.value:
            return VoyageProvider(
                api_key = self.config.VOYAGE_API_KEY,
                default_input_max_characters = self.config.INPUT_DEFAULT_MAX_CHARACTERS,
                default_generation_max_output_tokens = self.config.GENERATION_DEFAULT_MAX_TOKENS,
                default_generation_temperature = self.config.GENERATION_DEFAULT_TEMPERATURE
            )
        
        return None