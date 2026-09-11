from .providers import QdrantDBProvider
from .VectorDBEnums import VectorDBType
from controllers.BaseController import BaseController
from typing import Any


class VectorDBProviderFactory:
    def __init__(self, config: Any):
        self.config = config
        self.base_controller = BaseController()
        
    def create(self, provider: str) -> Any:
        if provider == VectorDBType.QDRANT.value:
            db_path = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_BACKEND)
            return QdrantDBProvider(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        return None

        