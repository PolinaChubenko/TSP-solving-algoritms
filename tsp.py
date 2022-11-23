import math
from typing import NamedTuple, List, Tuple


class TSP:
    class City(NamedTuple):
        id: str
        x: float
        y: float

    class State(NamedTuple):
        visited: int  # bit mask of visited nodes
        current_node: int

    def __init__(self, cities: List[City]):
        self.cities = cities

    @property
    def cities_amount(self):
        return len(self.cities)

    def successors(self, state: State) -> List[Tuple[State, float]]:
        """Successor function.

        Given the state we check which nodes have not been visited and add them.
        When all nodes have been visited, we must come back to the starting node.
        """
        ret: List[Tuple[TSP.State, float]] = []

        for next_node in range(0, len(self.cities)):
            new_state = TSP.State(1 << next_node | state.visited, next_node)

            if state.visited != new_state.visited:
                ret.append((new_state, self.dist(state.current_node, next_node)))

        if len(ret) == 0:
            # We must return now.
            return [(TSP.State(state.visited, 0), self.dist(state.current_node, 0))]

        return ret

    def goal(self, state) -> bool:
        """Determine whether the current state is a goal state.

        We are in a goal state if every node has been visited, and we are
        back at the starting node. Since we are representing the visited nodes
        with bits, this is equivalent to all bits set.
        """
        goal = (1 << len(self.cities)) - 1
        return state.visited == goal and state.current_node == 0

    def dist(self, u: int, v: int) -> float:
        """Euclidean distance between cities."""
        dx = self.cities[u].x - self.cities[v].x
        dy = self.cities[u].y - self.cities[v].y
        return math.sqrt(dx * dx + dy * dy)
