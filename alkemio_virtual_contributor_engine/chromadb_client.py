import logging
import chromadb
from chromadb.config import Settings

from alkemio_virtual_contributor_engine.config import env

logger = logging.getLogger(__name__)

if env.db_host and env.db_auth_credentials:
    chromadb_client = chromadb.HttpClient(
        host=env.db_host,
        port=env.db_port,
        ssl=False,
        settings=Settings(
            chroma_client_auth_provider=(
                "chromadb.auth.basic_authn.BasicAuthClientProvider"
            ),
            chroma_client_auth_credentials=env.db_auth_credentials,
        ),
    )
else:
    logger.warning(
        "Vector DB credentials not provided (VECTOR_DB_HOST / VECTOR_DB_CREDENTIALS). "
        "ChromaDB client not initialized."
    )
    chromadb_client = None
