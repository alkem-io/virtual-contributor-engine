import logging
from typing import Optional, List

from langchain_core.documents import Document

from .chromadb_client import chromadb_client
from .models import embeddings
from .utils import combine_documents

logger = logging.getLogger(__name__)


def query_documents(
    query: str,
    collection_name: str,
    num_docs: int = 4,
    include: Optional[list[str]] = None,
):
    """Query a ChromaDB collection by embedding a query string.

    Args:
        query: The text to embed and search for.
        collection_name: Name of the ChromaDB collection.
        num_docs: Number of results to return.
        include: Fields to include in results (e.g. ["documents", "metadatas", "distances"]).
    """
    if not chromadb_client:
        logger.error("ChromaDB client not initialized")
        return {}
    if not embeddings:
        logger.error("Embeddings model not initialized")
        return {}

    try:
        collection = chromadb_client.get_collection(
            collection_name, embedding_function=None
        )
        query_embedding = embeddings.embed_query(query)
        kwargs = {
            "query_embeddings": [query_embedding],
            "n_results": num_docs,
        }
        if include is not None:
            kwargs["include"] = include
        return collection.query(**kwargs)
    except Exception as e:
        logger.error(
            f"Error querying collection {collection_name} for query `{query}`"
        )
        logger.exception(e)
        return {}


def combine_query_results(docs, document_separator="\n\n", with_source_index=True):
    """Combine ChromaDB query result documents into a single string.

    Extracts the documents list from a ChromaDB query result dict
    and delegates to combine_documents.

    Args:
        docs: ChromaDB query result dict with "documents" key.
        document_separator: Separator between documents.
        with_source_index: If True, prefix each chunk with [source:N].
    """
    if not docs or "documents" not in docs:
        return ""

    documents = docs.get("documents")
    if not documents or not documents[0]:
        return ""

    filtered = [doc for doc in documents[0] if doc]

    if with_source_index:
        filtered = [f"[source:{i}] {doc}" for i, doc in enumerate(filtered)]

    return combine_documents(filtered, document_separator)


def ingest_documents(
    collection_name: str,
    documents: List[Document],
    batch_size: int = 10,
):
    """Ingest LangChain Documents into a ChromaDB collection.

    Replaces the collection if it already exists, then embeds and upserts
    documents in batches.

    Args:
        collection_name: Name of the ChromaDB collection.
        documents: List of LangChain Document objects with metadata containing "documentId".
        batch_size: Number of documents to embed and upsert per batch.
    """
    if not chromadb_client:
        raise RuntimeError("ChromaDB client not initialized — cannot ingest documents")
    if not embeddings:
        raise RuntimeError("Embeddings model not initialized — cannot ingest documents")

    try:
        chromadb_client.delete_collection(collection_name)
        logger.info(f"Collection {collection_name} deleted.")
    except Exception:
        logger.info(f"Collection {collection_name} not found, creating new.")

    collection = chromadb_client.get_or_create_collection(
        collection_name, embedding_function=None
    )
    logger.info(f"Collection {collection.name} created.")

    for batch_index in range(0, len(documents), batch_size):
        batch = documents[batch_index: batch_index + batch_size]
        texts = [doc.page_content for doc in batch]
        metadatas = [doc.metadata for doc in batch]
        ids = []
        for i, doc in enumerate(batch):
            doc_id = doc.metadata.get("documentId")
            if not doc_id:
                raise ValueError(
                    f"Document at index {batch_index + i} missing required 'documentId' in metadata"
                )
            ids.append(doc_id)

        logger.info(f"Embedding {len(texts)} documents")
        batch_embeddings = embeddings.embed_documents(texts)

        logger.info(f"Upserting {len(texts)} documents")
        collection.upsert(
            documents=texts,
            embeddings=list(batch_embeddings),
            metadatas=metadatas,
            ids=ids,
        )
        logger.info(f"Upserted {len(texts)} documents")
