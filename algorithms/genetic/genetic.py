from creation import *
from selection import *
from mutation import *
from crossover import *
from tsp import TSP


class Species:
    def __init__(self, path: np.array):
        self.path = path
        self.fitness = self._get_fitness()

    def path(self) -> np.array:
        return self.path

    def fitness(self) -> float:
        return self.fitness

    def set_path(self, path):
        self.path = path
        self.fitness = self._get_fitness()

    def _get_fitness(self) -> float:
        return TSP.path_length(self.path)


class GeneticAlgorithm:
    class Settings:
        elitist: int = 3
        population_size: int = 10  # Number of chromosomes.
        iterations: int = 500
        survived: float = 0.6  # fraction of survived species after selection
        mutated: float = 0.3  # fraction of mutated species
        creation: Creation
        selection: Selection
        crossover: Crossover
        mutation: Mutation

    def __init__(self, settings: Settings = Settings()):
        self.settings = settings

    def solve(self, tsp):
        population = self.settings.creation.generate_population(...)  # TODO
        alltime_killed = np.array([])

        for i in range(self.settings.iterations):
            # selection
            population, killed = self.settings.selection.select(population)
            alltime_killed = np.append(alltime_killed, killed)

            # crossover
            population = self.settings.crossover.crossover(population)

            # mutation
            population = self.settings.mutation.make_mutations(population)


