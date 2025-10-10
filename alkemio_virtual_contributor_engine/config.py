from typing import Literal, Optional
from pydantic import Field, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

load_dotenv()


class Env(BaseSettings):
    """Pydantic configuration class for RabbitMQ environment variables.

    Attributes:
        rabbitmq_host: The RabbitMQ server host
        rabbitmq_user: The RabbitMQ username
        rabbitmq_password: The RabbitMQ password
        rabbitmq_input_queue: The input queue name
        rabbitmq_result_queue: The result queue name
        rabbitmq_exchange: The exchange name
        rabbitmq_result_routing_key: The routing key for results
        db_host: The vector database host
        db_port: The vector database port
        db_auth_credentials: The vector database authentication credentials
        openai_key: The OpenAI API key
        openai_api_version: The OpenAI API version
        embeddings_model_name: The embeddings model name
        mistral_endpoint: The Mistral API endpoint
        mistral_key: The Mistral API key
        log_level: The logging level
        local_path: The local path
    """

    model_config = SettingsConfigDict(
        populate_by_name=True,
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # Required fields (from environment variables)
    rabbitmq_host: str = Field(..., alias="RABBITMQ_HOST")
    rabbitmq_user: str = Field(..., alias="RABBITMQ_USER")
    rabbitmq_password: str = Field(..., alias="RABBITMQ_PASSWORD")
    rabbitmq_input_queue: str = Field(..., alias="RABBITMQ_QUEUE")
    rabbitmq_result_queue: str = Field(..., alias="RABBITMQ_RESULT_QUEUE")
    rabbitmq_exchange: str = Field(
        ..., alias="RABBITMQ_EVENT_BUS_EXCHANGE"
    )
    rabbitmq_result_routing_key: str = Field(
        ..., alias="RABBITMQ_RESULT_ROUTING_KEY"
    )
    db_host: str = Field(..., alias="VECTOR_DB_HOST")
    db_auth_credentials: str = Field(..., alias="VECTOR_DB_CREDENTIALS")

    # Optional fields with defaults
    db_port: int = Field(default=8765, alias="VECTOR_DB_PORT")
    local_path: str = Field(default="./", alias="LOCAL_PATH")
    log_level: Literal[
        "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"
    ] = Field(
        default="INFO", alias="LOG_LEVEL"
    )

    # Optional fields without defaults in original (setting to None)
    openai_key: Optional[str] = Field(
        default=None, alias="AZURE_OPENAI_API_KEY"
    )
    openai_api_version: Optional[str] = Field(
        default=None, alias="OPENAI_API_VERSION"
    )
    openai_endpoint: Optional[str] = Field(
        default=None, alias="AZURE_OPENAI_ENDPOINT"
    )
    embeddings_model_name: Optional[str] = Field(
        default=None, alias="EMBEDDINGS_DEPLOYMENT_NAME"
    )

    mistral_endpoint: Optional[str] = Field(
        default=None, alias="AZURE_MISTRAL_ENDPOINT"
    )
    mistral_key: Optional[str] = Field(
        default=None, alias="AZURE_MISTRAL_API_KEY"
    )


env = Env()  # type: ignore[call-arg]
