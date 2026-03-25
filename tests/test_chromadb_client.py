from alkemio_virtual_contributor_engine.chromadb_client import chromadb_client


def test_chromadb_client_none_without_creds():
    """Without VECTOR_DB_HOST/VECTOR_DB_CREDENTIALS, client should be None."""
    assert chromadb_client is None
