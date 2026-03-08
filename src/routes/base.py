from fastapi import FastAPI, APIRouter, Depends
import os
from helpers.config import get_settings, Settings

base_router = APIRouter(
    prefix="/api/v1",
    tags=["api_v1"]
)

@base_router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    #app_settings = get_settings()
    
    app_name = app_settings.App_Name
    app_version = app_settings.App_Version
    
    return {
            "app name": app_name,
            "app version": app_version
            }