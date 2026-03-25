"""State class for managing the graph execution state."""

from typing import Any, Dict, Type
from pydantic import BaseModel
from .json_graph_parser import parse_json_graph


class State:
    """Factory for building dynamic state models from JSON schema definitions.

    The actual state model is created at runtime via build_state_model()
    and used by LangGraph as the graph's state type.
    """

    @staticmethod
    def build_state_model(state_schema: Dict[str, Any]) -> Type[BaseModel]:
        """Build a dynamic Pydantic model from a state schema definition."""
        return parse_json_graph(state_schema)
