# Graph manual import

from . import Graph, Node, Edge
from typing import TypedDict
import networkx as nx

class GraphEdgeDict(TypedDict):
    u: int
    v: int
    process: str


class GraphNodeDict(TypedDict):
    id: int
    ingredient: str
    is_original: bool
    is_final: bool


class GraphDict(TypedDict):
    name: str
    nodes: list[GraphNodeDict]
    edges: list[GraphEdgeDict]


def graph_from_dict(graphdict: GraphDict) -> Graph:
    digraph = nx.DiGraph()
    nodes: dict[int, Node] = {}
    for node in graphdict["nodes"]:
        digraph.add_node(node["id"])
        nodes[node["id"]] = (Node(node["ingredient"], node["is_original"], node["is_final"]))
    for edge in graphdict["edges"]:
        digraph.add_edge(edge["u"], edge["v"], data=Edge(edge["process"]))

    return Graph(graphdict["name"], nodes, digraph)
