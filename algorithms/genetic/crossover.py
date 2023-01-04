import random
from abc import ABC, abstractmethod

from algorithms.genetic.species import Species


class ParentGenerator(ABC):
    @abstractmethod
    def generate(self, population):
        pass


class InbreedingParentGenerator(ParentGenerator):
    def generate(self, population):
        sorted_population = sorted(population)

        for i in range(0, len(sorted_population) - 1, 2):
            yield sorted_population[i], sorted_population[i + 1]


class Crossover(ABC):
    def generate_two_children(self, first_parent, second_parent) -> (Species, Species):
        return self.generate_offspring(first_parent, second_parent), self.generate_offspring(second_parent, first_parent)

    @abstractmethod
    def generate_offspring(self, first_parent, second_parent) -> Species:
        pass


class OrderCrossover(Crossover):
    """takes random substring from one parent and fills the rest with cities from other parent considering order"""
    def generate_offspring(self, first_parent: Species, second_parent: Species) -> Species:
        path_length = first_parent.size()
        start, finish = random.randint(0, path_length - 1), random.randint(0, path_length - 1)
        if start > finish:
            start, finish = finish, start

        new_path = list(range(path_length))
        used = set()
        for i in range(start, finish):
            new_path[i] = first_parent.get_path()[i]
            used.add(new_path[i])

        last_index = finish % path_length
        for i in range(path_length):
            index = (finish + i) % path_length
            if second_parent.get_path()[index] not in used:
                new_path[last_index] = second_parent.get_path()[index]
                last_index = (last_index + 1) % path_length

        return Species(new_path)
