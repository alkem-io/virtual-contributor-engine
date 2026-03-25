import logging
from langchain_openai import OpenAIEmbeddings
from langchain_mistralai import ChatMistralAI
from pydantic import SecretStr
from .config import env

logger = logging.getLogger(__name__)

try:
    embeddings = OpenAIEmbeddings(
        openai_api_key=SecretStr(env.embeddings_api_key) if env.embeddings_api_key else None,
        openai_api_base=env.embeddings_endpoint,
        model=env.embeddings_model_name,
        check_embedding_ctx_length=False,
    )
except Exception as e:
    logger.warning(f"Embeddings not initialized: {e}")
    embeddings = None

try:
    mistral_small = ChatMistralAI(
        api_key=SecretStr(env.mistral_api_key) if env.mistral_api_key else None,
        model=env.mistral_small_model_name,
    )
except Exception as e:
    logger.warning(f"Mistral small model not initialized: {e}")
    mistral_small = None
