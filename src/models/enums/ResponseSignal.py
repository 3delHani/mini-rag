from enum import Enum

class ResponseSignal(Enum):
    
    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_TYPE_NOT_SUPPORTED = "File type is not supported."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed limit."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    FILE_PROCESSING_SUCCESS = "File processed successfully."
    FILE_PROCESSING_FAILED = "File processing failed."
    NO_FILES_ERROR = "Not found files."
    FILE_ID_ERROR = "No File found with this id."
    PROJECT_NOT_FOUND_ERROR = "Project not found."
    INSERT_INTO_VECTOR_DB_ERROR = "insert into vector db error."
    INSERT_INTO_VECTOR_DB_SUCCESS = "insert into vector db success."
    VECTORDB_COLLECTION_RETRIEVED = "VectorDB collection retrieved successfully."
    VECTORDB_SEARCH_SUCCESS = "VectorDB search completed successfully."
    VECTORDB_SEARCH_ERROR = "VectorDB search failed."
    