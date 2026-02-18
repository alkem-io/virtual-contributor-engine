from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from pydantic import SecretStr
from .config import env

openai_embeddings = AzureOpenAIEmbeddings(
    api_key=SecretStr(env.openai_key) if env.openai_key else None,
    api_version=env.openai_api_version,
    azure_endpoint=env.openai_endpoint,
    azure_deployment=env.embeddings_model_name,
)

# Note: Using AzureChatOpenAI instead of AzureAIChatCompletionsModel from langchain-azure-ai
# due to a dependency conflict. langchain-azure-ai requires numpy>=2.1.0 for Python 3.13+,
# but Poetry doesn't handle environment markers correctly and conflicts with
# chromadb-client 0.6.2 which requires numpy<2.0.0.
# Azure hosts Mistral models via an OpenAI-compatible API, so AzureChatOpenAI works fine.
mistral_medium = AzureChatOpenAI(
    api_key=SecretStr(env.mistral_key) if env.mistral_key else None,
    azure_endpoint=env.mistral_endpoint,
    azure_deployment=env.mistral_model_name,
    api_version=env.mistral_api_version,
)

mistral_large = AzureChatOpenAI(
    api_key=SecretStr(env.mistral_key) if env.mistral_key else None,
    azure_endpoint=env.mistral_endpoint,
    azure_deployment=env.mistral_large_model_name or env.mistral_model_name,
    api_version=env.mistral_api_version,
)
