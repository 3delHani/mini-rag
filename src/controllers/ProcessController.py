from .BaseController import BaseController
from .ProjectController import ProjectController
import os
from typing import Any, Dict
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
#from langchain_core.document import Document
from models import ProcessingEnum

class ProcessController(BaseController):
    
    def __init__(self, Project_id: str):
        super().__init__()
        
        self.project_id = Project_id
        self.project_path = ProjectController().get_project_path(project_id=Project_id)
    
    def get_file_extension(self, file_id: str):
        return os.path.splitext(file_id)[-1]     
        
    def get_file_loader(self, file_id: str):
        
        file_ext = self.get_file_extension(file_id=file_id)
        file_path = os.path.join(self.project_path, file_id)
        
        if not os.path.exists(file_path):
            return None
        
        if file_ext == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        
        if file_ext == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        
        return None
    
    def get_file_content(self, file_id: str):
        
        loader = self.get_file_loader(file_id=file_id)
        if loader is None:
            raise ValueError(f"Unsupported file type for file: {file_id}")
        return loader.load()
    
    def process_file_content(self, file_content: list[Any], file_id: str,
                             chunk_size: Any = 100, overlap_size: int = 20):
        
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                       chunk_overlap=overlap_size,
                                                       length_function=len,
                                                       )
        
        file_content_texts: list[str] = [
            rec.page_content for rec in file_content  
        ]
        
        file_content_metadata: list[Dict[str, Any]] = [
            rec.metadata for rec in file_content #type: ignore
        ]
        
        chucks = text_splitter.create_documents(file_content_texts,
                                                metadatas=file_content_metadata)
        
        return chucks
        