from qdrant_client import models, QdrantClient
from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceMethodEnums
import logging
from typing import Any, Dict, List, Optional

class QdrantDBProvider(VectorDBInterface):
    
    DISTANCE_MAPPING = {
        DistanceMethodEnums.COSINE.value: models.Distance.COSINE,
        DistanceMethodEnums.DOT.value: models.Distance.DOT,
    }

    def __init__(self, db_path: str, distance_method: str):

        self.client: Optional[QdrantClient] = None
        self.db_path = db_path

        normalized = (distance_method or "").strip().lower()
        if normalized not in self.DISTANCE_MAPPING:
            supported = ", ".join(sorted(self.DISTANCE_MAPPING.keys()))
            raise ValueError(
                f"Unsupported distance method {distance_method!r} for Qdrant. "
                f"Supported values: {supported}."
            )
        self.distance_method: Any = self.DISTANCE_MAPPING[normalized]

        self.logger = logging.getLogger(__name__)
        
    def connect(self):
        self.client = QdrantClient(path=self.db_path)
        
    def disconnect(self):
        self.client = None
        
    def is_collection_existed(self, collection_name: str) -> bool:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        return self.client.collection_exists(collection_name=collection_name)
    
    def list_all_collections(self) -> List[Any]:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        return self.client.get_collections().collections
    
    def get_collection_info(self, collection_name: str) -> Any:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        return self.client.get_collection(collection_name=collection_name)
    
    def delete_collection(self, collection_name: str) -> bool:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        if self.is_collection_existed(collection_name):
            return self.client.delete_collection(collection_name=collection_name)
        return False
    
    def create_collection(self, collection_name: str,
                                embedding_size: int,
                                do_reset: bool = False) -> None:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        if do_reset:
            self.delete_collection(collection_name=collection_name)
        
        if not self.is_collection_existed(collection_name=collection_name):
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config=models.VectorParams(
                                                   size=embedding_size,
                                                   distance=self.distance_method
                                    )
            )
            
    def insert_one(self, collection_name: str, text: str, vector: List[float],
                         metadata: Dict[str, Any], 
                         record_id: Any = None) -> bool:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        if not self.is_collection_existed(collection_name=collection_name):
            self.logger.error(f"can not insert a new record to non-existed collection: {collection_name}")
            return False
        
        try:
            _ = self.client.upsert(
                collection_name=collection_name,
                points=[
                    models.PointStruct(
                        id=record_id,
                        vector=vector,
                        payload={"text": text, "metadata": metadata}
                    )
                ]
            )
        except Exception as e:
            self.logger.error(f"error while inserting record: {e}")
            return False
        
        return True
    
    def insert_many(self, collection_name: str, texts: List[str], vectors: List[List[float]],
                             metadata: List[Any] | None = None,
                             record_ids: List[Any] | None = None,
                             batch_size: int = 50) -> Any :
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        if metadata is None:
            metadata = [None] * len(texts)
            
        if record_ids is None:
            record_ids = [None ] * len(texts)
            
        for i in range(0, len(texts), batch_size):
            batch_end = i + batch_size
            
            batch_texts = texts[i: batch_end]
            batch_vectors = vectors[i: batch_end]
            batch_metadata = metadata[i: batch_end]
            
            batch_records = [
                models.PointStruct(
                    id=record_ids[x],
                    vector=batch_vectors[x],
                    payload={"text": batch_texts[x], "metadata": batch_metadata[x]}
                )
                
                for x in range(len(batch_texts))
            ]
            try:    
                _ = self.client.upsert(
                    collection_name=collection_name,
                    points=batch_records,
                )
            except Exception as e:
                self.logger.error(f"error while inserting batch: {e}")  
                return False  
            
        return True 
    
    def search_by_vector(self, collection_name: str, vector: List[float], limit: int = 10) -> Any:
        if self.client is None:
            raise ValueError("Client is not initialized")
        
        return self.client.query_points(
            collection_name=collection_name,
            query_vector=vector,
            limit=limit,
            with_payload=True
        )