import pytest

from alkemio_virtual_contributor_engine.events.input import (
    Input,
    HistoryItem,
    MessageSenderRole,
    ExternalMetadata,
    ExternalConfig,
    RoomDetails,
    ResultHandler,
    ResultHandlerAction,
    InvocationOperation,
)


@pytest.fixture
def valid_input_data():
    return {
        "engine": "test-engine",
        "userID": "user-1",
        "message": "hello",
        "history": [{"content": "hi", "role": "human"}],
        "displayName": "Test User",
        "personaID": "persona-1",
        "resultHandler": {"action": "postReply"},
    }


def test_input_parses_complete(valid_input_data):
    inp = Input(**valid_input_data)
    assert inp.engine == "test-engine"
    assert inp.user_id == "user-1"
    assert inp.message == "hello"
    assert len(inp.history) == 1
    assert inp.display_name == "Test User"
    assert inp.persona_id == "persona-1"


def test_input_body_of_knowledge_id_defaults_none(valid_input_data):
    inp = Input(**valid_input_data)
    assert inp.body_of_knowledge_id is None


def test_input_prompt_graph_defaults_none(valid_input_data):
    inp = Input(**valid_input_data)
    assert inp.prompt_graph is None


def test_input_with_prompt_graph(valid_input_data):
    valid_input_data["promptGraph"] = {"nodes": [], "edges": []}
    inp = Input(**valid_input_data)
    assert inp.prompt_graph == {"nodes": [], "edges": []}


def test_input_operation_defaults_query(valid_input_data):
    inp = Input(**valid_input_data)
    assert inp.operation == InvocationOperation.QUERY


def test_input_serialization_uses_aliases(valid_input_data):
    inp = Input(**valid_input_data)
    dumped = inp.model_dump()
    assert "userID" in dumped
    assert "displayName" in dumped
    assert "personaID" in dumped


def test_history_item_human():
    item = HistoryItem(content="hello", role="human")
    assert item.role == MessageSenderRole.HUMAN
    assert item.content == "hello"


def test_history_item_assistant():
    item = HistoryItem(content="hi there", role="assistant")
    assert item.role == MessageSenderRole.ASSISTANT


def test_external_metadata():
    meta = ExternalMetadata(threadId="thread-123")
    assert meta.thread_id == "thread-123"


def test_external_config():
    config = ExternalConfig(apiKey="key", assistantId="asst", model="gpt-4")
    assert config.api_key == "key"
    assert config.assistant_id == "asst"
    assert config.model == "gpt-4"


def test_room_details():
    details = RoomDetails(roomID="room-1", actorID="actor-1")
    assert details.room_id == "room-1"
    assert details.actor_id == "actor-1"
    assert details.thread_id is None


def test_result_handler():
    handler = ResultHandler(action="postReply")
    assert handler.action == ResultHandlerAction.POST_REPLY
    assert handler.room_details is None
