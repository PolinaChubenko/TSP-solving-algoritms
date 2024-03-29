from abc import ABC, abstractmethod
import numpy as np
import random
from .species import Species


class Mutation(ABC):
    def __init__(self, mutated: float):
        self.mutated = mutated

    def make_mutations(self, population: np.array) -> np.array:
        indexes = random.sample(list(range(len(population))), int(np.ceil(len(population) * self.mutated)))
        for index in indexes:
            population[index] = self.mutate(population[index])

        return population

    @abstractmethod
    def mutate(self, species: Species) -> Species:
        pass


class CloseSwapMutation(Mutation):
    def mutate(self, species: Species) -> Species:
        path = species.get_path()
        one = random.randint(0, len(path) - 1)
        two = (one + 1) % len(path)

        path[one], path[two] = path[two], path[one]
        species.set_path(path)

        return species


class SwapMutation(Mutation):
    def mutate(self, species: Species):
        path = species.get_path()
        one = random.randint(0, len(path) - 1)
        two = random.randint(0, len(path) - 1)

        path[one], path[two] = path[two], path[one]
        species.set_path(path)

        return species


class ScrambleMutation(Mutation):
    def mutate(self, species: Species) -> Species:
        path = species.get_path()
        one = random.randint(0, len(path) - 1)
        two = random.randint(0, len(path) - 1)

        if one > two:
            one, two = two, one

        subpath = path[one:two]
        np.random.shuffle(subpath)
        path[one:two] = subpath

        species.set_path(path)
        return species


class TwoOptMutation(Mutation):
    def __init__(self, mutated: float, k: int = 1):
        super().__init__(mutated)
        self.k = k

    def mutate(self, species: Species) -> Species:
        for i in range(self.k):
            a = random.randint(0, species.size() - 1)
            c = (a + 2 + random.randint(0, species.size() - 4)) % species.size() # cannot choose A and B
            if a > c:
                a, c = c, a

            b = a + 1
            d = c + 1

            path = np.copy(species.get_path())
            path = np.append(path, path)
            bc = path[b:c + 1]
            ad = np.array(list(reversed(path[d:species.size() + a + 1])))
            new_path = np.append(ad, bc)

            species.set_path(new_path)

            return species


