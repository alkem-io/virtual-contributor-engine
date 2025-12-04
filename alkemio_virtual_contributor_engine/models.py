from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from pydantic import SecretStr
from .config import env

openai_embeddings = AzureOpenAIEmbeddings(
    api_key=SecretStr(env.openai_key) if env.openai_key else None,
    api_version=env.openai_api_version,
    azure_endpoint=env.openai_endpoint,
    azure_deployment=env.embeddings_model_name,
)

mistral_medium = AzureChatOpenAI(
    api_key=SecretStr(env.mistral_key) if env.mistral_key else None,
    azure_endpoint=env.mistral_endpoint or "",
    azure_deployment=env.mistral_model_name,
    api_version=env.mistral_api_version,
)
