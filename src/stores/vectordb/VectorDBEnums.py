from enum import Enum

class VectorDBType(Enum):
    QDRANT = "QDRANT"
    
class DistanceMethodEnums(Enum):
    COSINE = "cosine"
    DOT = "dot"