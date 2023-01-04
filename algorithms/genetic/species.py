from tsp import TSP
import numpy as np


class Species:
    tsp = None

    def __init__(self, path: np.array):
        self.path = path
        self.fitness = self._calculate_fitness()

    @staticmethod
    def set_tsp(tsp_to_set: TSP):
        Species.tsp = tsp_to_set

    def get_path(self) -> np.array:
        return self.path

    def size(self) -> int:
        return len(self.path)

    def get_fitness(self) -> float:
        return self.fitness

    def set_path(self, path):
        self.path = path
        self.fitness = self._calculate_fitness()

    def _calculate_fitness(self) -> float:
        return Species.tsp.path_length(self.path)

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()

