from unittest.mock import MagicMock

from alkemio_virtual_contributor_engine.utils import (
    get_language_by_code,
    combine_documents,
    clear_tags,
    entry_as_string,
    history_as_text,
    history_as_conversation,
    history_as_dict,
)
from alkemio_virtual_contributor_engine.events.input import (
    HistoryItem,
    MessageSenderRole,
)


def test_get_language_by_code_known():
    assert get_language_by_code("EN") == "English"
    assert get_language_by_code("FR") == "French"
    assert get_language_by_code("DE") == "German"
    assert get_language_by_code("ES") == "Spanish"
    assert get_language_by_code("NL") == "Dutch"
    assert get_language_by_code("BG") == "Bulgarian"
    assert get_language_by_code("UA") == "Ukrainian"


def test_get_language_by_code_unknown():
    assert get_language_by_code("XX") == "English"
    assert get_language_by_code("") == "English"


def test_combine_documents_strings():
    result = combine_documents(["hello", "world"])
    assert result == "hello\n\nworld"


def test_combine_documents_custom_separator():
    result = combine_documents(["a", "b"], document_separator=" | ")
    assert result == "a | b"


def test_combine_documents_document_objects():
    doc1 = MagicMock()
    doc1.page_content = "content1"
    doc2 = MagicMock()
    doc2.page_content = "content2"
    result = combine_documents([doc1, doc2])
    assert result == "content1\n\ncontent2"


def test_combine_documents_mixed():
    doc = MagicMock()
    doc.page_content = "from doc"
    result = combine_documents(["plain", doc])
    assert result == "plain\n\nfrom doc"


def test_clear_tags():
    assert clear_tags("hello") == "hello"
    assert clear_tags("hello {world}") == "hello world"
    assert clear_tags("test [@user](link) end") == "test end"
    assert clear_tags("no - [link](url) here") == "no  here"


def test_entry_as_string_human():
    item = HistoryItem(content="hello", role="human")
    result = entry_as_string(item)
    assert result == "Human: hello"


def test_entry_as_string_assistant():
    item = HistoryItem(content="hi there", role="assistant")
    result = entry_as_string(item)
    assert result == "Assistant: hi there"


def test_history_as_text():
    history = [
        HistoryItem(content="hello", role="human"),
        HistoryItem(content="hi", role="assistant"),
    ]
    result = history_as_text(history)
    assert "Human: hello" in result
    assert "Assistant: hi" in result
    assert "\n" in result


def test_history_as_conversation():
    history = [
        HistoryItem(content="hello", role="human"),
        HistoryItem(content="hi", role="assistant"),
    ]
    result = history_as_conversation(history)
    assert "human: hello" in result
    assert "assistant: hi" in result


def test_history_as_dict():
    history = [
        HistoryItem(content="hello {tag}", role="human"),
        HistoryItem(content="hi", role="assistant"),
    ]
    result = history_as_dict(history)
    assert len(result) == 2
    assert result[0]["role"] == MessageSenderRole.HUMAN
    assert result[0]["content"] == "hello tag"
    assert result[1]["role"] == MessageSenderRole.ASSISTANT
