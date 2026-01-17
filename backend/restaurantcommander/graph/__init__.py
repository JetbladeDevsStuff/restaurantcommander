# Graph main

import uuid
import networkx as nx

# An edge represents a step from one ingredient to another
class Edge:
    process: str

    def __init__(self, process: str) -> None:
        self.process = process

# A node represents an ingredient in the graph
class Node:
    ingredient: str
    is_original: bool
    is_final: bool

    def __init__(self, ingredient: str, is_original: bool, is_final: bool) -> None:
        self.ingredient = ingredient
        self.is_original = is_original
        self.is_final = is_final

# The graph is the overall graph of a recipie from the ingredients to the final
# product
class Graph:
    name: str
    ingredients: list[int]
    product: int
    nodes: dict[int, Node]
    graph: nx.DiGraph

    def __init__(self, name: str, ingredients: list[int], product: int) -> None:
        self.name = name
        self.ingredients = ingredients
        self.product = product


