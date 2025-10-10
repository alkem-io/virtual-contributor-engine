from langchain_openai import AzureOpenAIEmbeddings
from langchain_mistralai.chat_models import ChatMistralAI
from pydantic import SecretStr
from .config import env

openai_embeddings = AzureOpenAIEmbeddings(
    api_key=SecretStr(env.openai_key) if env.openai_key else None,
    api_version=env.openai_api_version,
    azure_deployment=env.embeddings_model_name,
)

mistral_medium = ChatMistralAI(
    api_key=SecretStr(env.mistral_key) if env.mistral_key else None,
    endpoint=env.mistral_endpoint or "",
)
