"""Prompt Graph module for building and executing graph-based prompts.

This module provides classes for defining and executing graph-based prompt workflows:

- PromptGraph: Orchestrates the execution of nodes and edges
- Node: Represents a processing step with LLM interaction
- Edge: Defines connections between nodes
- State: Manages data flowing through the graph

Example:
    >>> from alkemio_virtual_contributor_engine import PromptGraph
    >>> graph = PromptGraph.from_dict(prompt_graph_json)
    >>> compiled = graph.compile(llm=model, special_nodes={"retrieve": my_retrieve_fn})
    >>> result = compiled.invoke(initial_state)
"""

from .edge import Edge
from .prompt_graph import PromptGraph
from .node import Node
from .state import State
from .json_graph_parser import parse_json_graph

__all__ = ["Edge", "PromptGraph", "Node", "State", "parse_json_graph"]
