# The current state of the kitchen

from ..graph import Graph
from ..chef import Chef

class State:
    recipe: Graph
    chefs: list[Chef]

