"""PromptGraph class for managing and executing prompt graphs."""
import time
import logging
from typing import Any, Dict, List, Optional, Type
from typing import Callable
from pydantic import BaseModel, Field, ConfigDict

from .node import Node
from .edge import Edge
from .state import State
from langgraph.graph import StateGraph, START, END
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser

logger = logging.getLogger(__name__)


class PromptGraph(BaseModel):
    """Represents a complete prompt graph with nodes, edges, and state.

    A PromptGraph orchestrates the execution flow through multiple nodes, managing
    state transitions and coordinating LLM interactions.

    Special nodes (e.g. "retrieve") are passed at compile time via the
    special_nodes parameter, keeping the graph definition generic.

    Attributes:
        nodes: Dictionary of nodes in the graph, keyed by node name
        edges: List of edges defining the graph structure
        start_node: Name of the starting node (default "START")
        end_node: Name of the ending node (default "END")
        state_model: Pydantic model class for graph state
    """

    nodes: Dict[str, Node] = Field(default_factory=dict, description="Graph nodes by name")
    edges: List[Edge] = Field(default_factory=list, description="Graph edges")
    start_node: str = Field("START", alias="start", description="Starting node name")
    end_node: str = Field("END", alias="end", description="Ending node name")
    state_model: Optional[Type[BaseModel]] = Field(
        None,
        exclude=True,
        description="Pydantic model for graph state"
    )

    model_config = ConfigDict(
        validate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PromptGraph":
        """Create a PromptGraph from a dictionary.

        Args:
            data: Dictionary containing graph definition

        Returns:
            PromptGraph instance
        """
        # Parse nodes
        nodes_dict = {}
        for node_data in data.get("nodes", []):
            node = Node(**node_data)
            nodes_dict[node.name] = node

        # Parse edges
        edges = [Edge(**edge_data) for edge_data in data.get("edges", [])]

        # Build state model from schema if provided
        state_model = None
        if "state" in data:
            state_model = State.build_state_model(data["state"])

        # Create graph
        graph = cls(
            nodes=nodes_dict,
            edges=edges,
            start=data.get("start", "START"),
            end=data.get("end", "END"),
            state_model=state_model,
        )
        return graph

    def __repr__(self) -> str:
        return (
            f"PromptGraph(nodes={len(self.nodes)}, edges={len(self.edges)}, "
            f"{self.start_node} -> {self.end_node})"
        )

    def validate_graph(self) -> List[str]:
        """Validate the graph structure and return any issues found."""
        errors = []
        valid_node_names = set(self.nodes.keys()) | {self.start_node, self.end_node}

        for edge in self.edges:
            if edge.from_node not in valid_node_names:
                errors.append(f"Edge references non-existent source node: {edge.from_node}")
            if edge.to_node not in valid_node_names:
                errors.append(f"Edge references non-existent destination node: {edge.to_node}")

        has_start_edge = any(edge.from_node == self.start_node for edge in self.edges)
        if not has_start_edge:
            errors.append(f"No edge from START node ({self.start_node})")

        has_end_edge = any(edge.to_node == self.end_node for edge in self.edges)
        if not has_end_edge:
            errors.append(f"No edge to END node ({self.end_node})")

        return errors

    def compile(self, llm, special_nodes: Optional[Dict[str, Callable]] = None):
        """Compile the prompt graph into a LangGraph graph instance.

        Args:
            llm: The language model to use for LLM nodes.
            special_nodes: Optional mapping of node names to callable functions
                          for nodes that require custom processing (e.g. "retrieve").
                          These bypass the standard prompt/LLM pipeline.
        """
        if special_nodes is None:
            special_nodes = {}

        if self.state_model is None:
            raise ValueError(
                "Cannot compile graph without a state model. "
                "Provide a 'state' schema in the graph definition."
            )
        compiled_graph = StateGraph(self.state_model)

        # Register nodes
        for node_name, node in self.nodes.items():
            if node_name in special_nodes:
                compiled_graph.add_node(node_name, special_nodes[node_name])
                continue

            def make_node_fn(node, llm):
                def node_fn(state):
                    parser = PydanticOutputParser(pydantic_object=node.output_model)
                    format_instructions = parser.get_format_instructions()

                    prompt_text = node.prompt
                    required_instr = "Output format instructions: {format_instructions}"
                    if required_instr not in prompt_text:
                        prompt_text = prompt_text + "\n\n" + required_instr

                    prompt = ChatPromptTemplate.from_template(prompt_text)
                    prompt = prompt.partial(format_instructions=format_instructions)

                    missing_vars = [var for var in node.input_variables if not hasattr(state, var)]
                    if missing_vars:
                        raise ValueError(
                            f"Node '{node.name}' is missing required input variables from state: "
                            f"{', '.join(missing_vars)}. Available state attributes: "
                            f"{', '.join(dir(state))}"
                        )

                    input_dict = {var: getattr(state, var) for var in node.input_variables}

                    if logger.isEnabledFor(logging.DEBUG):
                        compiled_prompt = prompt.format(**input_dict)
                        logger.debug(f"\n{node.name}: {compiled_prompt}\n")

                    start_time = time.time()

                    try:
                        chain = prompt | llm | parser
                        result = chain.invoke(input_dict)
                    except Exception as e:
                        duration = time.time() - start_time
                        logger.error(
                            f"LLM chain for node '{node.name}' "
                            f"failed after {duration:.2f}s: {e}"
                        )
                        raise RuntimeError(
                            f"Node '{node.name}' chain invocation "
                            f"failed: {e}"
                        ) from e

                    duration = time.time() - start_time
                    logger.debug(f"LLM chain for node '{node.name}' completed in {duration:.2f}s")

                    return result.model_dump()
                return node_fn
            compiled_graph.add_node(node_name, make_node_fn(node, llm))

        # Add edges
        for edge in self.edges:
            if edge.from_node == self.start_node:
                compiled_graph.add_edge(START, edge.to_node)
            elif edge.to_node == self.end_node:
                compiled_graph.add_edge(edge.from_node, END)
            else:
                compiled_graph.add_edge(edge.from_node, edge.to_node)

        return compiled_graph.compile()
