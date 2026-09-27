from fastapi import FastAPI
from routes import base, data, nlp
from helpers.config import get_settings
from contextlib import asynccontextmanager 
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
from stores.templates.template_parser import TemplateParser
from sqlalchemy.ext.asyncio import create_async_engine ,AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()
    
    postgres_conn = f"postgresql+asyncpg://{settings.POSTGRES_USERNAME}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_MAIN_DATABASE}"
    
    app.state.db_engine = create_async_engine(postgres_conn)
    
    app.state.db_client = sessionmaker(
        bind=app.state.db_engine, class_=AsyncSession, expire_on_commit=False,
    )

    app.state.template_parser = TemplateParser(
        language=settings.PRIMARY_LANG,
        default_language=settings.DEFAULT_LANG
    )

    llm_provider_factory = LLMProviderFactory(settings)
    vectordb_provider_factory = VectorDBProviderFactory(config=settings, db_client=app.state.db_client)

    # generation client
    app.state.generation_client = llm_provider_factory.create(provider=settings.GENERATION_BACKEND)
    app.state.generation_client.set_generation_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client
    app.state.embedding_client = llm_provider_factory.create(provider=settings.EMBEDDING_BACKEND)
    app.state.embedding_client.set_embedding_model(
        model_id=settings.EMBEDDING_MODEL_ID,
        embedding_size=settings.EMBEDDING_MODEL_SIZE,
    )

    # vector database client
    app.state.vectordb_client = vectordb_provider_factory.create(provider=settings.VECTOR_DB_BACKEND)
    await app.state.vectordb_client.connect()

    yield

    app.state.db_engine.dispose()
    app.state.vectordb_client.disconnect()


app = FastAPI(lifespan=lifespan)

app.include_router(base.base_router)
app.include_router(data.data_router)
app.include_router(nlp.nlp_router)