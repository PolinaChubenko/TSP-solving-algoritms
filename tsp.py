import math
from typing import NamedTuple, List, Tuple, Dict, Any
import numpy as np
from scipy.spatial import distance_matrix
from multipledispatch import dispatch
import time

class TSP:
    class City(NamedTuple):
        id: str
        x: float
        y: float

    class State(NamedTuple):
        visited: int  # bit mask of visited nodes
        current_node: int

    def __init__(self, cities: List[City]):
        self._solution = 0
        self.cities = cities
        self.dist_in_iterations = []
        self.timestamps_in_iterations = []
        self.solutions_history = []
        self.ants_dists = []
        self.start_time = time.time()

        cities_coords = np.array([[c.x, c.y] for c in self.cities])
        self.distance_matrix = distance_matrix(cities_coords, cities_coords)

    def clear_answer(self):
        self.solution = 0
        self.dist_in_iterations = []
        self.solutions_history = []
        self.ants_dists = []

    @property
    def cities_amount(self):
        return len(self.cities)

    def successors(self, current_state: State, final_state: State) -> List[Tuple[State, float]]:
        """Successor function.

        Given the state we check which nodes have not been visited and add them.
        When all nodes have been visited, we must come back to the starting node.
        """
        ret: List[Tuple[TSP.State, float]] = []

        for next_node in range(len(self.cities)):
            new_state = TSP.State(1 << next_node | int(current_state.visited), next_node)

            if current_state.visited != new_state.visited:
                ret.append((new_state, self.dist(current_state.current_node, next_node)))

        if len(ret) == 0:
            # We must return now.
            return [(TSP.State(current_state.visited, final_state.current_node),
                     self.dist(current_state.current_node, final_state.current_node))]

        return ret

    def goal(self, current_state: State, final_state: State) -> bool:
        """Determine whether the current state is a goal state.

        We are in a goal state if every node has been visited, and we are
        back at the starting node. Since we are representing the visited nodes
        with bits, this is equivalent to all bits set.
        """
        goal = (1 << len(self.cities)) - 1
        return current_state.visited == goal and current_state.current_node == final_state.current_node

    def dist(self, u: int, v: int) -> float:
        """Euclidean distance between cities."""
        return self.distance_matrix[u][v]

    def dists(self):
        """Get distance matrix"""
        return self.distance_matrix

    def cities_to_dict(self) -> Dict:
        """Get cities for TSP problem as dict"""
        cities_dict = {}
        for city in self.cities:
            cities_dict[str(city.id)] = [city.x, city.y]
        return cities_dict

    @dispatch(float)
    def add_ant_distance(self, dist: float):
        """Ant distance saving function

        After each ant finishes its route this function may be called
        to add found solution (distance) to the list of ants distances."""
        self.ants_dists.append(dist)

    @dispatch(int, int)
    def add_ant_distance(self, iters: int, ants: int):
        """Ant distance saving function

        List is being reshaped according to the launches"""
        self.ants_dists = np.array(self.ants_dists).reshape((iters, ants))

    def get_ants_distances(self):
        """Return array of dists for each ant"""
        return self.ants_dists

    def add_iteration(self, dist: float) -> None:
        """Iteration saving function

        After each iteration of the algorithm this function may be called
        to add found solution (distance) to the list of iterations."""
        self.dist_in_iterations.append(dist)
        self.timestamps_in_iterations.append(time.time() - self.start_time)

    def get_iterations(self) -> (List[float], List[float]):
        """Return list of dists for each iteration"""
        return self.dist_in_iterations, self.timestamps_in_iterations

    def add_to_history(self, path: List, dist: float) -> None:
        """History saving function

        Each time after finding a more optimal path, this function can be called
        to add better solution (path and distance) to the list of history.
        Note that path is saved as id for cities list """
        current_solution = []
        for state in path:
            current_solution.append(self.cities[state.current_node])
        generation = {
            'path': current_solution,
            'distance': dist
        }
        self.solutions_history.append(generation)

    def get_solutions_history(self) -> Tuple[List[List[List[int]]], List[float]]:
        """Return history of paths and history of dists"""
        paths_history, dists_history = [], []
        for solution in self.solutions_history:
            path_x, path_y = [], []
            for city in solution['path']:
                path_x.append(city.x)
                path_y.append(city.y)
            paths_history.append([path_x, path_y])
            dists_history.append(solution['distance'])
        return paths_history, dists_history

    def answer_path(self) -> List[Any]:
        """Return answer for TSP problem as path of id's"""
        answer = self.solutions_history[-1]['path']
        return [city.id for city in answer]

    @property
    def solution(self) -> float:
        """Return answer for TSP problem as found distance"""
        return self._solution

    @solution.setter
    def solution(self, result):
        self._solution = result

    def path_length(self, path) -> float:
        length = 0
        for i in range(len(path)):
            length += self.dist(path[i], path[(i + 1) % len(path)])
        return length
