import pytest
from unittest.mock import MagicMock
from pydantic import BaseModel

from alkemio_virtual_contributor_engine.prompt_graph.node import Node


@pytest.fixture
def sample_node():
    return Node(
        name="analyze",
        input_variables=["query"],
        prompt="Analyze: {query}",
        output={
            "type": "object",
            "properties": {
                "result": {"type": "string"},
            },
        },
    )


def test_node_builds_output_model(sample_node):
    assert sample_node.output_model is not None
    assert issubclass(sample_node.output_model, BaseModel)


def test_node_format_prompt(sample_node):
    state = MagicMock()
    state.query = "what is AI?"
    result = sample_node.format_prompt(state)
    assert result == "Analyze: what is AI?"


def test_node_format_prompt_missing_var(sample_node):
    state = MagicMock(spec=[])
    with pytest.raises(KeyError, match="Required input variable"):
        sample_node.format_prompt(state)


def test_node_validate_output(sample_node):
    result = sample_node.validate_output({"result": "success"})
    assert result.result == "success"


def test_node_validate_output_no_model():
    node = Node(name="empty", prompt="test")
    with pytest.raises(ValueError, match="No output model defined"):
        node.validate_output({"key": "value"})


def test_node_repr(sample_node):
    assert "analyze" in repr(sample_node)
    assert "query" in repr(sample_node)


def test_node_repr_no_inputs():
    node = Node(name="simple", prompt="test")
    assert "none" in repr(node)


def test_node_from_alias():
    node = Node(
        name="test",
        output={
            "type": "object",
            "properties": {"value": {"type": "string"}},
        },
    )
    assert node.output_schema == {
        "type": "object",
        "properties": {"value": {"type": "string"}},
    }
