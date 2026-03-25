import pytest
from unittest.mock import patch, MagicMock

from alkemio_virtual_contributor_engine.prompt_graph.prompt_graph import PromptGraph


@pytest.fixture
def sample_graph_data():
    return {
        "start": "START",
        "end": "END",
        "state": {
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "result": {"type": "string"},
            },
        },
        "nodes": [
            {
                "name": "analyze",
                "input_variables": ["query"],
                "prompt": "Analyze: {query}",
                "output": {
                    "type": "object",
                    "properties": {"result": {"type": "string"}},
                },
            }
        ],
        "edges": [
            {"from": "START", "to": "analyze"},
            {"from": "analyze", "to": "END"},
        ],
    }


def test_from_dict(sample_graph_data):
    graph = PromptGraph.from_dict(sample_graph_data)
    assert "analyze" in graph.nodes
    assert len(graph.edges) == 2
    assert graph.state_model is not None
    assert graph.start_node == "START"
    assert graph.end_node == "END"


def test_validate_graph_valid(sample_graph_data):
    graph = PromptGraph.from_dict(sample_graph_data)
    errors = graph.validate_graph()
    assert errors == []


def test_validate_graph_bad_node_ref():
    data = {
        "nodes": [],
        "edges": [
            {"from": "START", "to": "nonexistent"},
            {"from": "nonexistent", "to": "END"},
        ],
    }
    graph = PromptGraph.from_dict(data)
    errors = graph.validate_graph()
    assert any("non-existent" in e for e in errors)


def test_validate_graph_no_start_edge():
    data = {
        "nodes": [
            {
                "name": "node1",
                "prompt": "test",
                "output": {
                    "type": "object",
                    "properties": {"r": {"type": "string"}},
                },
            }
        ],
        "edges": [{"from": "node1", "to": "END"}],
    }
    graph = PromptGraph.from_dict(data)
    errors = graph.validate_graph()
    assert any("START" in e for e in errors)


def test_validate_graph_no_end_edge():
    data = {
        "nodes": [
            {
                "name": "node1",
                "prompt": "test",
                "output": {
                    "type": "object",
                    "properties": {"r": {"type": "string"}},
                },
            }
        ],
        "edges": [{"from": "START", "to": "node1"}],
    }
    graph = PromptGraph.from_dict(data)
    errors = graph.validate_graph()
    assert any("END" in e for e in errors)


def test_repr(sample_graph_data):
    graph = PromptGraph.from_dict(sample_graph_data)
    r = repr(graph)
    assert "PromptGraph" in r
    assert "nodes=1" in r
    assert "edges=2" in r


def test_compile_with_mocked_state_graph(sample_graph_data):
    graph = PromptGraph.from_dict(sample_graph_data)

    with patch(
        "alkemio_virtual_contributor_engine.prompt_graph.prompt_graph.StateGraph"
    ) as mock_sg:
        mock_instance = MagicMock()
        mock_sg.return_value = mock_instance
        mock_instance.compile.return_value = MagicMock()

        graph.compile(llm=MagicMock())

        mock_sg.assert_called_once_with(graph.state_model)
        mock_instance.add_node.assert_called()
        mock_instance.add_edge.assert_called()
        mock_instance.compile.assert_called_once()


def test_compile_with_special_nodes(sample_graph_data):
    graph = PromptGraph.from_dict(sample_graph_data)
    special_fn = MagicMock()

    with patch(
        "alkemio_virtual_contributor_engine.prompt_graph.prompt_graph.StateGraph"
    ) as mock_sg:
        mock_instance = MagicMock()
        mock_sg.return_value = mock_instance
        mock_instance.compile.return_value = MagicMock()

        graph.compile(
            llm=MagicMock(), special_nodes={"analyze": special_fn}
        )

        # The special node should be added directly
        mock_instance.add_node.assert_any_call("analyze", special_fn)
