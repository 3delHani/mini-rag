from .BaseController import BaseController
from models.db_schemes import Project, DataChunk
from stores.llm.LLMEnums import DocumentTypeEnum
from typing import Any, List
import json

class NLPController(BaseController):
    
    def __init__(self, vectordb_client: Any, embedding_client: Any,
                 generation_client: Any, template_parser: Any):
        super().__init__()
        self.vectordb_client = vectordb_client
        self.embedding_client = embedding_client
        self.generation_client = generation_client 
        self.template_parser = template_parser
    
    def create_collection_name(self, project_id: str) -> str:
        return f"collection_{self.vectordb_client.default_vector_size}_{project_id}".strip()
    
    async def reset_vector_db_collection(self, project: Project):
        
        collection_name = self.create_collection_name(project_id=project.project_id)
        return await self.vectordb_client.delete_collection(collection_name=collection_name)
    
    async def get_vector_collection_info(self, project: Project) -> Any:
        collection_name = self.create_collection_name(project_id=project.project_id)
        collection_info = await self.vectordb_client.get_collection_info(collection_name=collection_name)
        
        return collection_info
    
    async def index_into_vector_db(self, project: Project, chunks : List[DataChunk],
                                   chunks_ids: List[int],
                                   do_reset : bool = False) -> Any:
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]
        
        vectors = self.embedding_client.embed_text(text=texts,
                                             document_type=DocumentTypeEnum.DOCUMENT.value)
        
        _ = await self.vectordb_client.create_collection(collection_name=collection_name,
                                                   do_reset=do_reset,
                                                   embedding_size=self.embedding_client.embedding_size)
        
        _ = await self.vectordb_client.insert_many(collection_name=collection_name,
                                             texts=texts,
                                             vectors=vectors,
                                             metadata=metadata,
                                             record_ids=chunks_ids)
        
        
        
        return True
    
    async def search_vector_db(self, project: Project, text: str, limit: int = 4):
        query_vector = None
        collection_name = self.create_collection_name(project_id=project.project_id)
        
        vectors = self.embedding_client.embed_text(text=[str(text).strip()],
                                                  document_type=DocumentTypeEnum.QUERY.value)
        
        if not vectors or len(vectors) == 0:
            return False
        
        if isinstance(vectors, list) and len(vectors) > 0:
            query_vector = vectors[0]
            
        if not query_vector:
            return False
        
        results = await self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=query_vector,
            limit=limit
            )
        
        if not results:
            return False
        
        return json.loads(
                    json.dumps(results, default=lambda x: x.__dict__)
                )
        
    async def answer_rag_question(self, project: Project, query: str, limit: int = 4) -> Any:
        
        answer, full_prompt, chat_history = None, None, None
        retrieved_docs = await self.search_vector_db(project=project, text=query, limit=limit)
        
        if not retrieved_docs or len(retrieved_docs) == 0:
            return answer, full_prompt, chat_history
        
        system_prompt = self.template_parser.get("rag", "system_prompt")
        
        documents_prompt: List[str] = "\n".join([
            self.template_parser.get("rag", "document_prompt", {
                                "doc_num": idx + 1,
                                "chunk_text": self.generation_client.process_text(doc.get("text") if isinstance(doc, dict) else getattr(doc, "text", "")),
                            })
            for idx, doc in enumerate(retrieved_docs)
        ])
        
        footer_prompt = self.template_parser.get("rag", "footer_prompt")
        
        chat_history = [
            self.generation_client.construct_prompt(
                prompt=system_prompt,
                role=self.generation_client.enums.SYSTEM.value,
            )
        ]
        
        full_prompt = "\n\n".join(documents_prompt) + "\n\n" + footer_prompt
        
        answer = self.generation_client.generate_text(
            prompt=full_prompt,
            chat_history=chat_history,
        )
        
        return answer, full_prompt, chat_history