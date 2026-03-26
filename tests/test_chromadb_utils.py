import pytest
from unittest.mock import patch, MagicMock
from langchain_core.documents import Document


def test_query_documents_no_client():
    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client", None
    ):
        from alkemio_virtual_contributor_engine.chromadb_utils import query_documents
        result = query_documents("test", "collection")
        assert result == {}


def test_query_documents_no_embeddings():
    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        MagicMock(),
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings", None
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                query_documents,
            )
            result = query_documents("test", "collection")
            assert result == {}


def test_query_documents_success():
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_collection.query.return_value = {"documents": [["doc1", "doc2"]]}

    mock_embeddings = MagicMock()
    mock_embeddings.embed_query.return_value = [0.1, 0.2, 0.3]

    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        mock_client,
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings",
            mock_embeddings,
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                query_documents,
            )
            result = query_documents("test query", "my-collection", num_docs=2)
            assert result == {"documents": [["doc1", "doc2"]]}
            mock_embeddings.embed_query.assert_called_once_with("test query")


def test_query_documents_with_include():
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_collection.query.return_value = {}

    mock_embeddings = MagicMock()
    mock_embeddings.embed_query.return_value = [0.1]

    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        mock_client,
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings",
            mock_embeddings,
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                query_documents,
            )
            query_documents("q", "col", include=["documents", "distances"])
            call_kwargs = mock_collection.query.call_args[1]
            assert call_kwargs["include"] == ["documents", "distances"]


def test_query_documents_exception():
    mock_client = MagicMock()
    mock_client.get_collection.side_effect = Exception("fail")
    mock_embeddings = MagicMock()

    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        mock_client,
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings",
            mock_embeddings,
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                query_documents,
            )
            result = query_documents("q", "col")
            assert result == {}


def test_combine_query_results_with_docs():
    from alkemio_virtual_contributor_engine.chromadb_utils import (
        combine_query_results,
    )
    docs = {"documents": [["hello", "world"]]}
    result = combine_query_results(docs)
    assert "[source:0] hello" in result
    assert "[source:1] world" in result


def test_combine_query_results_no_source_index():
    from alkemio_virtual_contributor_engine.chromadb_utils import (
        combine_query_results,
    )
    docs = {"documents": [["hello", "world"]]}
    result = combine_query_results(docs, with_source_index=False)
    assert "[source:" not in result
    assert "hello" in result


def test_combine_query_results_empty():
    from alkemio_virtual_contributor_engine.chromadb_utils import (
        combine_query_results,
    )
    assert combine_query_results(None) == ""
    assert combine_query_results({}) == ""
    assert combine_query_results({"documents": None}) == ""
    assert combine_query_results({"documents": [[]]}) == ""


def test_ingest_documents_no_client():
    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client", None
    ):
        from alkemio_virtual_contributor_engine.chromadb_utils import (
            ingest_documents,
        )
        with pytest.raises(RuntimeError, match="ChromaDB client not initialized"):
            ingest_documents("col", [])


def test_ingest_documents_no_embeddings():
    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        MagicMock(),
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings", None
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                ingest_documents,
            )
            with pytest.raises(
                RuntimeError, match="Embeddings model not initialized"
            ):
                ingest_documents("col", [])


def test_ingest_documents_success():
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_collection.name = "test-col"
    mock_client.get_or_create_collection.return_value = mock_collection

    mock_embeddings = MagicMock()
    mock_embeddings.embed_documents.return_value = [[0.1], [0.2]]

    docs = [
        Document(page_content="doc1", metadata={"documentId": "id1"}),
        Document(page_content="doc2", metadata={"documentId": "id2"}),
    ]

    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        mock_client,
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings",
            mock_embeddings,
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                ingest_documents,
            )
            ingest_documents("test-col", docs)
            mock_collection.upsert.assert_called_once()
            mock_embeddings.embed_documents.assert_called_once()


def test_ingest_documents_missing_document_id():
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_collection.name = "test-col"
    mock_client.get_or_create_collection.return_value = mock_collection

    mock_embeddings = MagicMock()

    docs = [Document(page_content="doc1", metadata={})]

    with patch(
        "alkemio_virtual_contributor_engine.chromadb_utils.chromadb_client",
        mock_client,
    ):
        with patch(
            "alkemio_virtual_contributor_engine.chromadb_utils.embeddings",
            mock_embeddings,
        ):
            from alkemio_virtual_contributor_engine.chromadb_utils import (
                ingest_documents,
            )
            with pytest.raises(ValueError, match="missing required 'documentId'"):
                ingest_documents("test-col", docs)
