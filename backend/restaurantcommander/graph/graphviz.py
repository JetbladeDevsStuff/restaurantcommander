# Turns a graph into a graphviz graph

from . import Graph
from graphviz import Digraph

def create_gv_from_graph(graph: Graph) -> Digraph:
    dot = Digraph(graph.name)
    for node in graph.nodes:
        dot.node(str(node), graph.nodes[node].ingredient)
    for edge in graph.graph.edges.data():
        dot.edge(edge[0], edge[1], str(edge[2]))
    return dot

def render_and_show_graph(dot: Digraph):
    dot.render(view=True)

