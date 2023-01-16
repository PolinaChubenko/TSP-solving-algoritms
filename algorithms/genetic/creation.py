import random
from abc import ABC, abstractmethod
import numpy as np
from algorithms.genetic.species import Species
from tsp import TSP


class Creation(ABC):
    def __init__(self, size: int):
        self.size = size

    @abstractmethod
    def generate_population(self, length: int) -> np.array:
        pass


class RandomCreation(Creation):
    def __int__(self, size: int):
        super().__init__(size)

    def generate_population(self, length: int) -> np.array:
        population = []
        for i in range(self.size):
            species = Species(np.random.permutation(length))
            population.append(species)

        return np.array(population)


class EfficientCreation(Creation):
    def __init__(self, size: int, tsp: TSP, clever_paths: float = 0.5, randomness: int = 5):
        super().__init__(size)
        self.dists = np.array(tsp.dists())
        self.dists = np.argsort(self.dists, axis=0)
        self.clever_paths = clever_paths
        self.randomness = randomness

    def generate_population(self, length: int) -> np.array:
        population = []
        clever_count = int(self.clever_paths * self.size)
        for i in range(clever_count):
            population.append(Species(self.generate_clever_path(length)))

        for i in range(self.size - clever_count):
            species = Species(np.random.permutation(length))
            population.append(species)

        return np.array(population)

    def generate_clever_path(self, length) -> np.array:
        path = []
        used = np.zeros(length)
        start = random.randint(0, length - 1)
        used[start] = 1
        used_count = 1
        path.append(start)
        for i in range(length - 1):
            path.append(self.get_next(path[-1], length, used, used_count))

        return np.array(path)

    def get_next(self, v: int, length: int, used: np.array, used_count: int) -> int:
        available = length - used_count
        selected = []
        i = 0
        while len(selected) < min(available, self.randomness) and i < length:
            if not used[self.dists[i][v]]:
                selected.append(self.dists[i][v])

            i += 1

        index = random.choice(selected)
        used[index] = 1
        used_count += 1
        return index
