from .creation import Creation
from .selection import Selection
from .mutation import Mutation
from .crossover import ParentGenerator, Crossover
from .species import Species
from tsp import TSP
import numpy as np


class GeneticAlgorithm:
    class Settings:
        # elitist: int = 3
        population_size: int = 100  # Number of chromosomes.
        iterations: int = 30
        survived: float = 0.6  # fraction of survived species after selection
        mutated: float = 0.3  # fraction of mutated species
        creation: Creation
        selection: Selection
        crossover: Crossover
        parent_selector: ParentGenerator
        mutation: Mutation

    def __init__(self, settings: Settings = Settings()):
        self.settings = settings

    def solve(self, tsp: TSP) -> float:
        Species.set_tsp(tsp)
        population = self.settings.creation.generate_population(tsp.cities_amount)  # TODO
        alltime_killed = np.array([])
        best_answer = None
        print("created", len(population))

        for i in range(self.settings.iterations):
            # selection
            population, killed = self.settings.selection.select(population)
            alltime_killed = np.append(alltime_killed, killed)
            # print("selected", len(population))

            # crossover
            children = []
            for first_parent, second_parent in self.settings.parent_selector.generate(population): # TODO allow killed to crossover
                first_child, second_child = self.settings.crossover.generate_two_children(first_parent, second_parent)
                children.append(first_child)
                children.append(second_child)

            population = np.append(population, children)

            # mutation
            population = self.settings.mutation.make_mutations(population)

            # normalize population and save history
            population = np.sort(population)
            if (best_answer is None) or (population[0] < best_answer):
                best_answer = population[0]

            print(i, len(population))

        return best_answer.get_fitness()


