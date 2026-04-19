from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any
from bson import ObjectId

class DataChunk(BaseModel):
    id: Optional[ObjectId] = Field(default=None, alias="_id")
    chunk_text: str = Field(..., min_length=1)
    chunk_metadata: Dict[str, Any] = Field(default_factory=dict)
    chunk_order: int = Field(..., gt=0)
    chunk_project_id: Optional[ObjectId] = Field(None)

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)
    
    @classmethod
    def get_indexes(cls) -> list[dict[str, list[tuple[str, int]] | str | bool]]:
        
        return [
            {
                "key":[
                    ("chunck_project_id", 1)
                ],
                "name":"chunck_project_id_index_1",
                "unique": False
            }
        ]