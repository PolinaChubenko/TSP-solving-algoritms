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
    def select(self, population: np.array, k: int = 2) -> np.array:
        n = len(population)
        killed = []
        while len(population) > self.survived * n:
            get_sample = random.sample(list(range(len(population))), k)
            max_index = max(get_sample, key=lambda x: population[x].fitness())
            for index in get_sample:
                if index != max_index:
                    killed.append(population.pop(index))

        return population, killed


class RouletteSelection(Selection):
    def select(self, population: np.array) -> np.array:
        fitnesses = np.array(list(map(lambda x: x.fitness(), population)))
        summa = np.sum(fitnesses)
        probs = fitnesses / summa
        distr = sps.bernoulli(probs)
        is_keeping = distr.rvs() == 1
        return population[is_keeping], population[np.logical_not(is_keeping)]


class RankSelection(Selection):
    def select(self, population: np.array, a: float = 1):
        fitnesses = np.array(list(map(lambda x: x.fitness(), population)))
        order = np.flip(np.argsort(fitnesses))
        n = len(population)
        b = 2 - a
        probs = (a - (a - b) * order / (n - 1)) / n
        distr = sps.bernoulli(probs)
        is_keeping = distr.rvs() == 1
        return population[is_keeping], population[np.logical_not(is_keeping)]





