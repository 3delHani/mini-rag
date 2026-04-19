from .BaseDataModel import BaseDataModel
from .db_schemes import DataChunk 
from .enums.DataBaseEnum import DataBaseEnum
from bson.objectid import ObjectId
from typing import Any
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client: object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
        
    @classmethod
    async def create_instance(cls, db_client: object) -> "ChunkModel":
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance
        
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_CHUNK_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
            indexes = DataChunk.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
        
    async def create_chunk(self, chunk: DataChunk) -> Any:
        result = await self.collection.insert_one(chunk.model_dump(by_alias=True, exclude_unset=True))
        chunk.id = result.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id: str) -> Any:
        result = await self.collection.find_one({"_id": ObjectId(chunk_id)})
        
        if result is None:
            return None
        
        return DataChunk(**result)
    
    async def insert_many_chunks(self, chunks: list[DataChunk], batch_size: int=100):
        
        for i in range(0, len(chunks), batch_size):
            batch = chunks[i:i + batch_size]
            
            operations = [
                InsertOne(chunk.model_dump(by_alias=True, exclude_none=True, exclude={"_id"}))
                for chunk in batch
            ]
            
            await self.collection.bulk_write(operations, ordered=False)
            
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id: str):
        result = await self.collection.delete_many({
            "chunk_project_id": project_id
            })
        
        return result.deleted_count