from alkemio_virtual_contributor_engine.events.response import Response, Source


def test_response_minimal():
    r = Response()
    assert r.result is None
    assert r.sources == []
    assert r.thread_id is None


def test_response_with_result():
    r = Response(result="hello", humanLanguage="en")
    assert r.result == "hello"
    assert r.human_language == "en"


def test_response_with_sources():
    source = Source(documentId="doc-1", title="Test", score=0.95)
    r = Response(result="ok", sources=[source])
    assert len(r.sources) == 1
    assert r.sources[0].document_id == "doc-1"
    assert r.sources[0].score == 0.95


def test_response_serialization():
    r = Response(result="ok", humanLanguage="en", resultLanguage="en")
    dumped = r.model_dump()
    assert "humanLanguage" in dumped
    assert "resultLanguage" in dumped


def test_source_model():
    s = Source(
        chunkIndex=1,
        embeddingType="ada",
        documentId="doc-1",
        source="file.txt",
        title="Title",
        type="text",
        score=0.8,
        uri="https://example.com",
    )
    assert s.chunk_index == 1
    assert s.embedding_type == "ada"
    assert s.uri == "https://example.com"


def test_source_all_optional():
    s = Source()
    assert s.chunk_index is None
    assert s.document_id is None
    assert s.score is None
