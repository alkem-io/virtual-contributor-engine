from alkemio_virtual_contributor_engine.events.ingest_website import (
    IngestWebsite,
    SummarizationModel,
)
from alkemio_virtual_contributor_engine.events.ingest_website_result import (
    IngestWebsiteResult,
    IngestionResult,
)


def test_ingest_website():
    iw = IngestWebsite(
        baseUrl="https://example.com",
        type="website",
        purpose="test",
        personaId="persona-1",
    )
    assert iw.base_url == "https://example.com"
    assert iw.type == "website"
    assert iw.purpose == "test"
    assert iw.persona_id == "persona-1"


def test_ingest_website_default_summarization_model():
    iw = IngestWebsite(
        baseUrl="https://example.com",
        type="website",
        purpose="test",
        personaId="persona-1",
    )
    assert iw.summarization_model == SummarizationModel.MISTRAL_MEDIUM


def test_ingest_website_custom_summarization_model():
    iw = IngestWebsite(
        baseUrl="https://example.com",
        type="website",
        purpose="test",
        personaId="persona-1",
        summarizationModel="mistral-large",
    )
    assert iw.summarization_model == SummarizationModel.MISTRAL_LARGE


def test_ingest_website_serialization():
    iw = IngestWebsite(
        baseUrl="https://example.com",
        type="website",
        purpose="test",
        personaId="persona-1",
    )
    dumped = iw.model_dump()
    assert "baseUrl" in dumped
    assert "personaId" in dumped


def test_ingest_website_result_defaults():
    result = IngestWebsiteResult()
    assert result.result == IngestionResult.SUCCESS
    assert result.error == ""
    assert result.timestamp > 0


def test_ingest_website_result_failure():
    result = IngestWebsiteResult(
        result="failure", error="Something went wrong"
    )
    assert result.result == "failure"
    assert result.error == "Something went wrong"


def test_ingestion_result_enum():
    assert IngestionResult.SUCCESS.value == "success"
    assert IngestionResult.FAILURE.value == "failure"


def test_summarization_model_enum():
    assert SummarizationModel.MISTRAL_MEDIUM.value == "mistral-medium"
    assert SummarizationModel.MISTRAL_LARGE.value == "mistral-large"
