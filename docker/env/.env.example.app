APP_NAME="mini-RAG"
APP_VERSION="0.1.0"
OPENAI_API_KEY=""

FILE_ALLOWED_TYPES=["text/plain", "application/pdf"]
FILE_MAX_SIZE_MB=10
FILE_DEFAULT_CHUNK_SIZE=512000

POSTGRES_USERNAME = ""
POSTGRES_PASSWORD = ""
POSTGRES_HOST = "pgvector"
POSTGRES_PORT = 5432
POSTGRES_MAIN_DATABASE = "minirag"

# ===================================== Llm configs =====================================
GENERATION_BACKEND="OPENAI"
EMBEDDING_BACKEND="COHERE"

OPENAI_API_KEY=""
OPENAI_API_URL= ""
COHERE_API_KEY=""
VOYAGE_API_KEY=""

GENERATION_MODEL_ID_LITERAL = ["gpt-4o-mini", "gpt-4o", "gemma3:4b"]
GENERATION_MODEL_ID="gemma3:4b"
EMBEDDING_MODEL_ID="embed-multilingual-v3.0"
EMBEDDING_MODEL_SIZE=1024

INPUT_DEFAULT_MAX_CHARACTERS=1024
GENERATION_DEFAULT_MAX_TOKENS=200
GENERATION_DEFAULT_TEMPERATURE=0.1

# ============================== Vector db configs ==============================
VECTOR_DB_BACKEND_LITERAL = ["QDRANT", "PGVECTOR"]
VECTOR_DB_BACKEND = "PGVECTOR"
VECTOR_DB_PATH = "qdrant_db"
VECTOR_DB_DISTANCE_METHOD = "cosine"
VECTOR_DB_PGVEC_INDEX_THRESHOLD = 300

# ============================== Template configs ==============================
PRIMARY_LANG = "en"
DEFAULT_LANG = "en"