from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from typing import Any
from bson import ObjectId

class AssetModel(BaseDataModel):
    
    def __init__(self, db_client: Any):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
        
    @classmethod
    async def create_instance(cls, db_client: object) -> "AssetModel":
        instance = cls(db_client=db_client)
        await instance.init_collection()
        return instance
    
    async def init_collection(self):
        all_collections = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collections:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Asset.get_indexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
                
    async def create_asset(self, asset: Asset) -> Asset:
        
        result = await self.collection.insert_one(asset.model_dump(by_alias=True, exclude_none=True))
        asset.id = result.inserted_id
        
        return asset
    
    async def get_all_project_asset(self, asset_project_id: Any) -> Asset | None:
        
        return await self.collection.find_one({
            "asset_project_id": ObjectId(asset_project_id) if isinstance(asset_project_id, str) else asset_project_id
        }).to_list(length=None)
    
    