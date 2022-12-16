from abc import ABC, abstractmethod


class Crossover(ABC):
    def crossover(self, population):
        pass

    @abstractmethod
    def select_parents(self, population):
        pass

    @abstractmethod
    def generate_offspring(self, parent1, parent2):
        pass

