import os

# Set required env vars BEFORE any module imports happen (at collection time).
# These are needed because config.py runs `env = Env()` at import time.
os.environ.setdefault("RABBITMQ_HOST", "localhost")
os.environ.setdefault("RABBITMQ_USER", "guest")
os.environ.setdefault("RABBITMQ_PASSWORD", "guest")
os.environ.setdefault("RABBITMQ_QUEUE", "test_input")
os.environ.setdefault("RABBITMQ_RESULT_QUEUE", "test_result")
os.environ.setdefault("RABBITMQ_EVENT_BUS_EXCHANGE", "test_exchange")
os.environ.setdefault("RABBITMQ_RESULT_ROUTING_KEY", "test.routing.key")
os.environ.setdefault("LOG_LEVEL", "WARNING")
