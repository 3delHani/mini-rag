from .BaseController import BaseController
from .ProjectController import ProjectController
from fastapi import UploadFile
from models import ResponseSignal
import re
import os

class DataController(BaseController):
    
    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # Convert MB to Bytes
        
    def validate_uploaded_file(self, file: UploadFile):
        
        # Implement validation logic for the uploaded file
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        
        if file.size > self.app_settings.FILE_MAX_SIZE_MB * self.size_scale:
            return False, ResponseSignal.FILE_SIZE_EXCEEDED.value
        
        return True, ResponseSignal.FILE_VALIDATION_SUCCESS.value
    
    def generate_unique_filename(self, original_filename: str, project_id: str):
        
        random_key = self.generate_random_string()
        project_path = ProjectController().get_project_path(project_id=project_id)
        
        cleanned_file_name = self.get_clean_filename(original_filename=original_filename)
        
        new_file_path = os.path.join(project_path, random_key + "_" + cleanned_file_name)
        
        while os.path.exists(os.path.join(project_path, new_file_path)):
            
            random_key = self.generate_random_string()
            new_file_path = os.path.join(random_key + "_" + cleanned_file_name)
        
        return new_file_path, random_key + "_" + cleanned_file_name    
        
    def get_clean_filename(self, original_filename: str):
        clean_file_name = re.sub(r'[^\w.]', '', original_filename)
        
        clean_file_name = clean_file_name.replace(' ', '_')
        
        return clean_file_name
        