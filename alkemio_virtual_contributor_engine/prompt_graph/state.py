"""State class for managing the graph execution state."""

from typing import Any, Dict, Type
from pydantic import BaseModel, ConfigDict
from .json_graph_parser import parse_json_graph


class State(BaseModel):
    """Represents the state that flows through the prompt graph during execution.

    The state is dynamically created from the JSON schema definition and holds
    all data that is passed between nodes during graph execution.
    """
    model_config = ConfigDict(
        extra="allow",
        arbitrary_types_allowed=True,
    )

    @classmethod
    def build_state_model(cls, state_schema: Dict[str, Any]) -> Type[BaseModel]:
        """Build a dynamic Pydantic model from a state schema definition."""
        state_model = parse_json_graph(state_schema)
        return state_model

    def update(self, **kwargs: Any) -> "State":
        """Update the state with new values."""
        current_data = self.model_dump()
        current_data.update(kwargs)
        return self.__class__(**current_data)

    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state."""
        return getattr(self, key, default)
