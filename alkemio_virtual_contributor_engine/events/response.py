
from typing import List, Optional
from pydantic import Field
from .base import Base

class Source(Base):
    chunk_index: Optional[int] = Field(None, alias="chunkIndex")
    embedding_type: Optional[str] = Field(None, alias="embeddingType")
    document_id: Optional[str] = Field(None, alias="documentId")
    source: Optional[str] = Field(None)
    title: Optional[str] = Field(None)
    type: Optional[str] = Field(None)
    score: Optional[float] = Field(None)
    uri: Optional[str] = Field(None)

class Response(Base):
    result: Optional[str] = Field(None)
    human_language: Optional[str] = Field(None, alias="humanLanguage")
    result_language: Optional[str] = Field(None, alias="resultLanguage")
    knowledge_language: Optional[str] = Field(None, alias="knowledgeLanguage")
    original_result: Optional[str] = Field(None, alias="originalResult")
    sources: List[Source] = Field(default_factory=list)
    thread_id: Optional[str] = Field(None, alias="threadId")
