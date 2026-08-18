from abc import ABC, abstractmethod 
from typing import List, Dict, Any
from models.db_schemes import RetrievedDocument

class VectorDBInterface(ABC):
    
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def disconnect(self):   
        pass
    
    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass
    
    @abstractmethod
    def list_all_collections(self) -> List[str]:
        pass
    
    @abstractmethod 
    def get_collection_info(self, collection_name: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def create_collection(self, collection_name: str,
                                embedding_size: int,
                                do_reset: bool = False):
        pass
    
    @abstractmethod
    def delete_collection(self, collection_name: str) -> bool :
        pass
    
    @abstractmethod
    def insert_one(self, collection_name: str, text: str, vector: List[float],
                             metadata: Dict[str, Any],
                             record_id: Any = None) -> bool:
        pass
    
    @abstractmethod
    def insert_many(self, collection_name: str, texts: List[str], vectors: List[List[float]],
                             metadata: List[Any] | None = None,
                             record_ids: List[Any] | None = None,
                             batch_size: int = 50):
        pass
    
    @abstractmethod
    def search_by_vector(self, collection_name: str, vector: List[float], limit: int = 10) -> List[RetrievedDocument]:
        pass