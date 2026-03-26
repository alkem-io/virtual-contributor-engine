import copy

import pytest
from pydantic import BaseModel

from alkemio_virtual_contributor_engine.prompt_graph.json_graph_parser import (
    _transform_schema,
    parse_json_graph,
)


def test_transform_schema_list_to_dict():
    schema = {
        "type": "object",
        "properties": [
            {"name": "query", "type": "string"},
            {"name": "count", "type": "integer"},
        ],
    }
    _transform_schema(schema)
    assert isinstance(schema["properties"], dict)
    assert "query" in schema["properties"]
    assert "count" in schema["properties"]
    assert "name" not in schema["properties"]["query"]


def test_transform_schema_optional_flag():
    schema = {
        "type": "object",
        "properties": [
            {"name": "result", "type": "string", "optional": True},
        ],
    }
    _transform_schema(schema)
    assert schema["properties"]["result"]["type"] == ["string", "null"]
    assert "optional" not in schema["properties"]["result"]


def test_transform_schema_optional_false_removed():
    schema = {
        "type": "object",
        "properties": [
            {"name": "required_field", "type": "string", "optional": False},
        ],
    }
    _transform_schema(schema)
    assert schema["properties"]["required_field"]["type"] == "string"
    assert "optional" not in schema["properties"]["required_field"]


def test_transform_schema_array_items():
    schema = {
        "type": "object",
        "properties": {
            "items_list": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": [
                        {"name": "value", "type": "string"},
                    ],
                },
            }
        },
    }
    _transform_schema(schema)
    items_props = schema["properties"]["items_list"]["items"]["properties"]
    assert isinstance(items_props, dict)
    assert "value" in items_props


def test_transform_schema_rejects_non_dict_property():
    schema = {
        "type": "object",
        "properties": ["not a dict"],
    }
    with pytest.raises(ValueError, match="must be a dict"):
        _transform_schema(schema)


def test_transform_schema_rejects_missing_name():
    schema = {
        "type": "object",
        "properties": [{"no_name_key": "value"}],
    }
    with pytest.raises(ValueError, match="missing required"):
        _transform_schema(schema)


def test_transform_schema_rejects_non_string_name():
    schema = {
        "type": "object",
        "properties": [{"name": 123, "type": "string"}],
    }
    with pytest.raises(ValueError, match="missing required"):
        _transform_schema(schema)


def test_transform_schema_rejects_duplicate_names():
    schema = {
        "type": "object",
        "properties": [
            {"name": "field", "type": "string"},
            {"name": "field", "type": "integer"},
        ],
    }
    with pytest.raises(ValueError, match="Duplicate property name"):
        _transform_schema(schema)


def test_parse_json_graph_produces_model():
    schema = {
        "type": "object",
        "properties": {
            "query": {"type": "string"},
            "result": {"type": "string"},
        },
    }
    model_cls = parse_json_graph(schema)
    assert issubclass(model_cls, BaseModel)


def test_parse_json_graph_model_instance():
    schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
        },
    }
    model_cls = parse_json_graph(schema)
    instance = model_cls(name="Alice", age=30)
    assert instance.name == "Alice"
    assert instance.age == 30


def test_parse_json_graph_does_not_mutate_input():
    schema = {
        "type": "object",
        "properties": [
            {"name": "field", "type": "string", "optional": True},
        ],
    }
    original_props = copy.deepcopy(schema["properties"])
    parse_json_graph(schema)
    assert schema["properties"] == original_props
