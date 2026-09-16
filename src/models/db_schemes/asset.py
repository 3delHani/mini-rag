from pydantic import BaseModel, Field
from typing import Optional, Any
from bson import ObjectId
from datetime import datetime, UTC

class Asset(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    asset_project_id: Optional[ObjectId] = Field(default=None)
    asset_type: str = Field(..., min_length=1)
    asset_name: str = Field(..., min_length=1)
    asset_size: int = Field(gt=0,)
    asset_config: dict[str, Any] = Field(default_factory=dict)
    asset_pushed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    class Config:
        arbitrary_types_allowed = True
        
    @classmethod
    def get_indexes(cls) -> list[dict[str, list[tuple[str, int]] | str | bool]]:
        
        return [
            {
                "key":[
                    ("asset_project_id", 1)
                ],
                "name":"asset_project_id_index_1",
                "unique": False
            },
            {
                "key":[
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                "name":"asset_project_id_name_index_1",
                "unique": True
            }
        ]
    