# Chef system

from ..graph import Graph
import networkx as nx


# A chef and his tasks
class Chef:
    name: str
    tasks: list[str]

def create_stepgraph(graph: Graph) -> nx.DiGraph:
    step_graph = nx.line_graph(graph.graph)
    step_graph = nx.relabel_nodes(step_graph, {edge: graph.graph.edges[edge].get("data", edge).process for edge in graph.graph.edges})


def topo_layers(G: nx.DiGraph) -> list:
    in_degree = dict(G.in_degree())
    layers = []
    ready = [n for n, d in in_degree.items() if d == 0]

    while ready:
        layers.append(ready)
        next_ready = []

        for node in ready:
            for succ in G.successors(node):
                in_degree[succ] -= 1
                if in_degree[succ] == 0:
                    next_ready.append(succ)

        ready = next_ready

    return layers


def split_graph_among_chefs(graph: Graph, chefs: list[Chef]) -> list[Chef]:
    stepgraph = create_stepgraph(graph)
    layers = topo_layers(stepgraph)
    on_chef_idx = 0

    for layer in layers:
        on_chef_idx = 0
        for i in layer:
            chefs[on_chef_idx].tasks.append(i)
            on_chef_idx += 1
            if on_chef_idx > len(chefs):
                on_chef_idx = 0

    return chefs

