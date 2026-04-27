from fastapi import FastAPI
from routes import base, data
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from contextlib import asynccontextmanager 
from stores.LLMProviderFactory import LLMProviderFactory

    
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    app.state.mongo_client = AsyncIOMotorClient(settings.MONGODB_URL) 
    app.state.db_client = app.state.mongo_client[settings.MONGODB_DATABASE]
    
    llm_provider_factory = LLMProviderFactory(settings)
    
    # generation client
    
    app.state.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.state.generation_client.set_generation_model(model_id = settings.GENERATION_MODEL_ID)
    
    # embedding client
    app.state.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding_model(model_id = settings.EMBEDDING_MODEL_ID,
                                                   embedding_size = settings.EMBEDDING_MODEL_SIZE)
    
    yield
    app.state.mongo_client.close()

app = FastAPI(lifespan=lifespan)
app.include_router(base.base_router)
app.include_router(data.data_router)