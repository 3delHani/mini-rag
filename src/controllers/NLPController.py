from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import Any, List
import json

class NLPController(BaseController):
    
    def __init__(self, vectordb_client: Any, embedding_client: Any, generation_client: Any):
        super().__init__()
        self.vectordb_client = vectordb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client 
    
    def create_collection_name(self, project_id: str) -> str:
        return f"project_{project_id}".strip()
    
    def reset_vector_db_collection(self, project: Project):
        
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)
    
    def get_vector_collection_info(self, project: Project) -> Any:
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return json.loads(
            json.dumps(collection_info, default=lambda x: x.__dict__)
        )
    
    def index_into_vector_db(self, project: Project, chunks : List[DataChunk],
                                   chunks_ids: List[int],
                                   do_reset : bool = False) -> Any:
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        
        vectors = [
            self.embedding_client.embed_text(text=text, document_type=DocumentTypeEnum.DOCUMENT.value)
            for text in texts
        ]
        
        _ = self.vectordb_client.create_collection(collection_name=collection_name,
                                                   do_reset=do_reset,
                                                   embedding_size=self.embedding_client.embedding_size)
        
        _ = self.vectordb_client.insert_many(collection_name=collection_name,
                                             texts=texts,
                                             vectors=vectors,
                                             metadata=metadata,
                                             record_ids=chunks_ids)
        
        return True
    
    def search_vector_db(self, project: Project, text: str, limit: int = 4):
        collection_name = self.create_collection_name(project_id=project.project_id)

        if text is None or not str(text).strip():
            return False
        
        vector = self.embedding_client.embed_text(text=str(text).strip(),
                                                  document_type=DocumentTypeEnum.QUERY.value)
        
        if not vector or len(vector) == 0:
            return False
        
        results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
            )
        
        if not results:
            return False
        
        return json.loads(
                    json.dumps(results, default=lambda x: x.__dict__)
                )