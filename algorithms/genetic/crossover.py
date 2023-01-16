import random
from abc import ABC, abstractmethod

from algorithms.genetic.species import Species
import numpy as np
import random

class ParentGenerator(ABC):
    @abstractmethod
    def generate(self, population: np.array, pairs: int):
        pass


class InbreedingParentGenerator(ParentGenerator):
    def generate(self, population: np.array, pairs: int):
        sorted_population = sorted(population)

        for i in range(pairs):
            index = random.randint(0, len(sorted_population) - 1)
            fitness = sorted_population[index].get_fitness()
            prev_fitness = sorted_population[(index - 1 + len(sorted_population)) % len(sorted_population)].get_fitness()
            next_fitness = sorted_population[(index + 1) % len(sorted_population)].get_fitness()
            if abs(fitness - prev_fitness) < abs(fitness - next_fitness):
                yield sorted_population[index], sorted_population[(index - 1 + len(sorted_population)) % len(sorted_population)]
            else:
                yield sorted_population[index], sorted_population[(index + 1) % len(sorted_population)]


class OutbreedingParentGenerator(ParentGenerator):
    def generate(self, population: np.array, pairs: int):
        first = np.argmin(population)
        last = np.argmax(population)

        for i in range(pairs):
            index = random.randint(0, len(population) - 1)
            fitness = population[i].get_fitness()
            if abs(fitness - population[first].get_fitness()) > abs(fitness + population[last].get_fitness()):
                yield population[i], population[first]
            else:
                yield population[i], population[last]


class PanmixiaParentGenerator(ParentGenerator):
    def generate(self, population: np.array, pairs: int):
        for i in range(pairs):
            first = random.randint(0, len(population) - 1)
            second = random.randint(0, len(population) - 1)
            yield population[first], population[second]


class Crossover(ABC):
    @abstractmethod
    def generate_offspring(self, first_parent: Species, second_parent: Species) -> Species:
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


class EdgeRecombinationCrossover(Crossover):
    """inherits as many edges from parents as possible"""
    class EdgeMap:
        class IncidentEdges:
            def __init__(self):
                self.set = set()
                self.not_used = 0

            def add(self, edge: int):
                self.set.add(edge)
                self.not_used += 1

            def use(self, edge: int):
                self.set.remove(edge)
                self.not_used -= 1

        def __init__(self, first: Species, second: Species):
            self.n = first.size()
            self.map = [self.IncidentEdges() for _ in range(first.size())]
            self.not_used = set(list(range(self.n)))
            self._add(first)
            self._add(second)

        def step(self, prev) -> int:
            # 1. find city with max not used incident edges
            min_value = -1
            min_index = []
            for i in self.map[prev].set:
                if min_value == -1 or 0 < self.map[i].not_used < min_value:
                    min_value = self.map[i].not_used
                    min_index = [i]
                elif self.map[i].not_used == min_value:
                    min_index.append(i)

            # 2. select one of these cities randomly
            if len(min_index) > 0:
                random_index = min_index[random.randint(0, len(min_index) - 1)]
            else:
                random_index = random.choice(list(self.not_used))

            # 3. delete it from other sets and clear
            for edge in self.map[random_index].set:
                self.map[edge].use(random_index)

            self.not_used.remove(random_index)

            return random_index

        def get_path(self) -> np.array:
            prev = -1
            path = []
            for i in range(self.n):
                path.append(self.step(prev))
                prev = path[-1]
            return path

        def _add(self, species: Species):
            size = species.size()
            for i in range(size):
                path = species.get_path()
                self.map[path[i]].add(path[(i + 1) % size])
                self.map[path[i]].add(path[(i - 1 + size) % size])

    def generate_offspring(self, first_parent: Species, second_parent: Species) -> Species:
        edge_map = self.EdgeMap(first_parent, second_parent)
        new_path = edge_map.get_path()

        return Species(new_path)
