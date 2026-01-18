# The current state of the kitchen

from networkx import DiGraph
from ..graph import Graph
from ..chef import Chef

class State:
    recipe: Graph
    chefs: list[Chef]

    def __init__(self) -> None:
        self.recipe = Graph("No recipe", dict(), DiGraph())
        self.chefs = []
