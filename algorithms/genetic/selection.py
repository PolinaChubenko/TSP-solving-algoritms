from abc import ABC, abstractmethod
import random
import numpy as np
import scipy.stats as sps


class Selection(ABC):
    def __init__(self, survived: float):
        self.survived = survived

    @abstractmethod
    def select(self, population: np.array) -> np.array:
        pass


class TournamentSelection(Selection):
    def __init__(self, survived: float, k: int = 2):
        super().__init__(survived)
        self.k = k

    def select(self, population: np.array) -> np.array:
        n = len(population)
        # killed = []
        while len(population) > self.survived * n:
            get_sample = random.sample(list(range(len(population))), self.k)
            max_index = max(get_sample, key=lambda x: population[x].get_fitness())
            for index in get_sample:
                if index != max_index:
                    # killed.append(population[index])
                    population = np.append(population[:index], population[index + 1:])

        return population


class RouletteSelection(Selection):
    def select(self, population: np.array) -> np.array:
        fitnesses = np.array(list(map(lambda x: x.get_fitness(), population)))
        max_fitness = np.max(fitnesses) + 1
        summa = np.sum(max_fitness - fitnesses)
        probs = (max_fitness - fitnesses) / summa

        return np.random.choice(population, int(np.ceil(len(population) * self.survived)), p=probs)


class RankSelection(Selection): # TODO сверить определение
    def select(self, population: np.array, a: float = 1) -> np.array:
        fitnesses = np.array(list(map(lambda x: x.get_fitness(), population)))
        order = np.argsort(fitnesses)
        n = len(population)
        b = 2 - a
        probs = (a - (a - b) * order / (n - 1)) / n

        return np.random.choice(population, int(np.ceil(len(population) * self.survived)), p=probs)





