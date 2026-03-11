from enum import Enum

class ResponseSignal(Enum):
    
    FILE_VALIDATION_SUCCESS = "File validation successful."
    FILE_TYPE_NOT_SUPPORTED = "File type is not supported."
    FILE_SIZE_EXCEEDED = "File size exceeds the maximum allowed limit."
    FILE_UPLOAD_SUCCESS = "File uploaded successfully."
    FILE_UPLOAD_FAILURE = "File upload failed."
    PROCESSING_SUCCESS = "File processed successfully."
    FILE_PROCESSING_FAILED = "File processing failed."