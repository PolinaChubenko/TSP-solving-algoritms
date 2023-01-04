from abc import ABC, abstractmethod
import numpy as np
import random
from .species import Species


class Mutation(ABC):
    def __init__(self, mutated: float):
        self.mutated = mutated

    def make_mutations(self, population: np.array):
        indexes = random.sample(list(range(len(population))), int(np.ceil(len(population) * self.mutated)))
        for index in indexes:
            population[index] = self.mutate(population[index])

        return population

    @abstractmethod
    def mutate(self, species: Species):
        pass


class CloseMutation(Mutation):
    def __init__(self, mutated: float):
        super().__init__(mutated)

    def mutate(self, species: Species):
        path = species.get_path()
        one = random.randint(0, len(path) - 1)
        two = (one + 1) % len(path)

        path[one], path[two] = path[two], path[one]
        species.set_path(path)

        return species
