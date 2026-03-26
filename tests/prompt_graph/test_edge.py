from alkemio_virtual_contributor_engine.prompt_graph.edge import Edge


def test_edge_from_aliases():
    e = Edge(**{"from": "START", "to": "node1"})
    assert e.from_node == "START"
    assert e.to_node == "node1"


def test_edge_from_field_names():
    e = Edge(from_node="START", to_node="node1")
    assert e.from_node == "START"
    assert e.to_node == "node1"


def test_edge_repr():
    e = Edge(from_node="A", to_node="B")
    assert repr(e) == "Edge(A -> B)"


def test_edge_serialization():
    e = Edge(from_node="START", to_node="END")
    dumped = e.model_dump(by_alias=True)
    assert dumped["from"] == "START"
    assert dumped["to"] == "END"
