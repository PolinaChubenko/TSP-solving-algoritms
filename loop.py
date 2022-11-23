from itertools import permutations
import numpy as np
from typing import Any, List, NamedTuple


class LoopSolution:
    class Trail(NamedTuple):
        path: List[Any]
        distance: float

    def __init__(self, cities_amount):
        self.adjacency_graph = np.zeros((cities_amount, cities_amount), dtype=float)
        self.best_solution = LoopSolution.Trail([], float('inf'))

    def solve(self, initial_state: Any, dist_fn) -> Trail:
        self.best_solution = LoopSolution.Trail([], float('inf'))

        it = np.nditer(self.adjacency_graph, flags=['multi_index'], op_flags=['readwrite'])
        for dist in it:
            dist[...] = dist_fn(it.multi_index[0], it.multi_index[1])

        vertex = []
        for i in range(self.adjacency_graph.shape[0]):
            if i != initial_state:
                vertex.append(i)

        next_permutation = permutations(vertex)
        for perm in next_permutation:
            current_path_weight = 0.0

            # compute current path weight
            k = initial_state
            for j in perm:
                current_path_weight += self.adjacency_graph[k][j]
                k = j
            current_path_weight += self.adjacency_graph[k][initial_state]

            if current_path_weight < self.best_solution.distance:
                path = [initial_state] + list(perm) + [initial_state]
                self.best_solution = LoopSolution.Trail(path, current_path_weight)

        return self.best_solution
