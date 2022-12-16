from abc import ABC, abstractmethod
import numpy as np
from genetic import Species


class Creation(ABC):
    def __init__(self, size: int):
        self.size = size

    @abstractmethod
    def generate_population(self, length: int):
        pass


class RandomCreation(Creation):
    def __int__(self, size: int):
        super().__init__(size)

    def generate_population(self, length: int):
        population = []
        for i in range(self.size):
            species = Species(np.random.permutation(length))
            population.append(species)

        return population
