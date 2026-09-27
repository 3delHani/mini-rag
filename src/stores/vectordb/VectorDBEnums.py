from enum import Enum

class VectorDBType(Enum):
    QDRANT = "QDRANT"
    PGVECTOR = "PGVECTOR"
    
class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"

class PgVectorTableSchemeEnums(Enum):
    ID = "id"
    TEXT = "text"
    VECTOR = "vector"
    CHUNKID = "chunk_id"
    METADATA = "metadata"
    _PREFIX = "pgvector"
    
class PgVectorDistanceMethodEnums(Enum):
    COSINE = "vector_cosine_ops"
    DOT = "vector_l2_ops"
    
class PgVectorIndexTypeEnums(Enum):
    IVFFLAT = "ivfflat"
    HNSW = "hnsw"