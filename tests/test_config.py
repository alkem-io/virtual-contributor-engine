from alkemio_virtual_contributor_engine.config import Env


def test_env_loads_required_fields(monkeypatch):
    monkeypatch.setenv("RABBITMQ_HOST", "myhost")
    monkeypatch.setenv("RABBITMQ_USER", "myuser")
    monkeypatch.setenv("RABBITMQ_PASSWORD", "mypass")
    monkeypatch.setenv("RABBITMQ_QUEUE", "myqueue")
    monkeypatch.setenv("RABBITMQ_RESULT_QUEUE", "myresult")
    monkeypatch.setenv("RABBITMQ_EVENT_BUS_EXCHANGE", "myexchange")
    monkeypatch.setenv("RABBITMQ_RESULT_ROUTING_KEY", "mykey")

    e = Env()
    assert e.rabbitmq_host == "myhost"
    assert e.rabbitmq_user == "myuser"
    assert e.rabbitmq_password == "mypass"
    assert e.rabbitmq_input_queue == "myqueue"
    assert e.rabbitmq_result_queue == "myresult"
    assert e.rabbitmq_exchange == "myexchange"
    assert e.rabbitmq_result_routing_key == "mykey"


def test_env_optional_defaults(monkeypatch):
    e = Env()
    assert e.db_port == 8765
    assert e.log_level in ("INFO", "WARNING")
    assert e.db_host is None
    assert e.db_auth_credentials is None
    assert e.embeddings_api_key is None
    assert e.embeddings_endpoint is None
    assert e.embeddings_model_name is None
    assert e.mistral_api_key is None
    assert e.mistral_small_model_name is None


def test_env_custom_optional_values(monkeypatch):
    monkeypatch.setenv("VECTOR_DB_HOST", "chromahost")
    monkeypatch.setenv("VECTOR_DB_PORT", "9999")
    monkeypatch.setenv("VECTOR_DB_CREDENTIALS", "token123")
    monkeypatch.setenv("EMBEDDINGS_API_KEY", "emb-key")
    monkeypatch.setenv("MISTRAL_API_KEY", "mist-key")
    monkeypatch.setenv("MISTRAL_SMALL_MODEL_NAME", "mistral-small-latest")

    e = Env()
    assert e.db_host == "chromahost"
    assert e.db_port == 9999
    assert e.db_auth_credentials == "token123"
    assert e.embeddings_api_key == "emb-key"
    assert e.mistral_api_key == "mist-key"
    assert e.mistral_small_model_name == "mistral-small-latest"


def test_env_log_level_values(monkeypatch):
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    e = Env()
    assert e.log_level == "DEBUG"
