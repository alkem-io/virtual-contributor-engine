import importlib
from unittest.mock import patch, MagicMock


def _reload_chromadb_client_with_env(mock_env, mock_http=None):
    """Reload chromadb_client module with a mocked env."""
    patches = [
        patch(
            "alkemio_virtual_contributor_engine.config.env",
            mock_env,
        ),
    ]
    if mock_http is not None:
        patches.append(patch("chromadb.HttpClient", return_value=mock_http))

    for p in patches:
        p.start()
    try:
        mod = importlib.import_module(
            "alkemio_virtual_contributor_engine.chromadb_client"
        )
        importlib.reload(mod)
        return mod
    finally:
        for p in patches:
            p.stop()


def test_chromadb_client_none_without_creds():
    """Without VECTOR_DB_HOST/VECTOR_DB_CREDENTIALS, client should be None."""
    mock_env = MagicMock()
    mock_env.db_host = None
    mock_env.db_auth_credentials = None

    mod = _reload_chromadb_client_with_env(mock_env)
    assert mod.chromadb_client is None


def test_chromadb_client_created_with_creds():
    """With VECTOR_DB_HOST and VECTOR_DB_CREDENTIALS, client is created."""
    mock_env = MagicMock()
    mock_env.db_host = "chromahost"
    mock_env.db_port = 8765
    mock_env.db_auth_credentials = "token123"

    mock_http_client = MagicMock()
    mod = _reload_chromadb_client_with_env(mock_env, mock_http_client)
    assert mod.chromadb_client is mock_http_client
