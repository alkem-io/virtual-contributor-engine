import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Env:
    """Configuration class for RabbitMQ environment variables.

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
    """

    rabbitmq_host: str
    rabbitmq_user: str
    rabbitmq_password: str
    rabbitmq_input_queue: str
    rabbitmq_result_queue: str
    rabbitmq_exchange: str
    rabbitmq_result_routing_key: str
    db_host: str
    db_port: int
    db_auth_credentials: str

    log_level: str
    local_path: str

    def __init__(self):

        # Required configurations
        required_vars = [
            "RABBITMQ_HOST",
            "RABBITMQ_USER",
            "RABBITMQ_PASSWORD",
            "RABBITMQ_QUEUE",
            "RABBITMQ_RESULT_QUEUE",
            "RABBITMQ_EVENT_BUS_EXCHANGE",
            "RABBITMQ_RESULT_ROUTING_KEY",
            "VECTOR_DB_HOST",
            "VECTOR_DB_CREDENTIALS",
        ]

        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )

        self.rabbitmq_host = os.getenv("RABBITMQ_HOST", "")
        self.rabbitmq_user = os.getenv("RABBITMQ_USER", "")
        self.rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "")
        self.rabbitmq_input_queue = os.getenv("RABBITMQ_QUEUE", "")
        self.rabbitmq_result_queue = os.getenv("RABBITMQ_RESULT_QUEUE", "")
        self.rabbitmq_exchange = os.getenv("RABBITMQ_EVENT_BUS_EXCHANGE", "")
        self.rabbitmq_result_routing_key = os.getenv("RABBITMQ_RESULT_ROUTING_KEY", "")

        self.db_host = os.getenv("VECTOR_DB_HOST", "")
        self.db_port = int(os.getenv("VECTOR_DB_PORT", "8765"))
        self.db_auth_credentials = os.getenv("VECTOR_DB_CREDENTIALS", "")

        self.local_path = os.getenv("LOCAL_PATH", "./")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        assert self.log_level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


env = Env()
