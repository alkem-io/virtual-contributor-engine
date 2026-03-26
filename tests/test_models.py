def test_embeddings_importable():
    from alkemio_virtual_contributor_engine.models import embeddings
    # embeddings may be None or an instance depending on env
    assert embeddings is None or embeddings is not None


def test_mistral_small_importable():
    from alkemio_virtual_contributor_engine.models import mistral_small  # noqa: F401
    # In test env without API keys, may be None
    # The key behavior is no exception at import time
    assert True
