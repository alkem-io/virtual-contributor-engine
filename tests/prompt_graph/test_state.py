from pydantic import BaseModel

from alkemio_virtual_contributor_engine.prompt_graph.state import State


def test_build_state_model_simple():
    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "result": {"type": "string"},
        },
    }
    model_cls = State.build_state_model(schema)
    assert issubclass(model_cls, BaseModel)


def test_build_state_model_has_fields():
    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "count": {"type": "integer"},
        },
    }
    model_cls = State.build_state_model(schema)
    fields = model_cls.model_fields
    assert "query" in fields
    assert "count" in fields


def test_build_state_model_instance():
    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
        },
    }
    model_cls = State.build_state_model(schema)
    instance = model_cls(query="hello")
    assert instance.query == "hello"
