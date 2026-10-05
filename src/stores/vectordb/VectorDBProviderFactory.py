from .providers import QdrantDBProvider, PGVectorProvider
from .VectorDBEnums import VectorDBType
from controllers.BaseController import BaseController
from sqlalchemy.orm import sessionmaker
from typing import Any


class VectorDBProviderFactory:
    def __init__(self, config: Any, db_client: sessionmaker[Any] = None):
        self.config = config
        self.base_controller = BaseController()
        self.db_client = db_client
        
    def create(self, provider: str) -> Any:
        if provider == VectorDBType.QDRANT.value:
            qdrant_db_client = self.base_controller.get_database_path(db_name=self.config.VECTOR_DB_BACKEND)
            return QdrantDBProvider(
                db_client=qdrant_db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD
            )
        
        if provider == VectorDBType.PGVECTOR.value:
            return PGVectorProvider(
                db_client=self.db_client,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
                default_vector_size=self.config.EMBEDDING_MODEL_SIZE,
                index_threshold=self.config.VECTOR_DB_PGVEC_INDEX_THRESHOLD
            )
            
        
        return None

        