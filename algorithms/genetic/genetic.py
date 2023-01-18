from dataclasses import dataclass

from .creation import Creation
from .selection import Selection
from .mutation import Mutation
from .crossover import ParentGenerator, Crossover
from .species import Species
from tsp import TSP
import numpy as np


class GeneticAlgorithm:
    @dataclass
    class Settings:
        creation: Creation
        selection: Selection
        crossover: Crossover
        parent_generator: ParentGenerator
        mutation: Mutation
        population_size: int = 1000  # Number of chromosomes.
        iterations: int = 500
        survived: float = 0.5  # fraction of survived species after selection
        mutated: float = 0.3  # fraction of mutated species

    def __init__(self, settings: Settings):
        self.settings = settings

    def solve(self, tsp: TSP) -> float:
        Species.set_tsp(tsp)
        population = self.settings.creation.generate_population(tsp.cities_amount)  # TODO
        # alltime_killed = np.array([])
        best_answer = None

        for i in range(self.settings.iterations):
            # selection
            population = self.settings.selection.select(population)
            # alltime_killed = np.append(alltime_killed, killed)

            # crossover
            children = []
            pairs = (self.settings.population_size - len(population))
            for first_parent, second_parent in self.settings.parent_generator.generate(population, pairs): # TODO allow killed to crossover?
                child = self.settings.crossover.generate_offspring(first_parent, second_parent)
                children.append(child)

            population = np.append(population, children)

            # mutation
            population = self.settings.mutation.make_mutations(population)

            # normalize population and save history
            population = np.sort(population)
            if (best_answer is None) or (population[0].get_fitness() < best_answer.get_fitness()):
                best_answer = population[0].copy()

            tsp.add_iteration(tsp.path_length(population[0].get_path()))
            best_answer_states = [TSP.State(0, best_answer.get_path()[i]) for i in range(len(best_answer.get_path()))]
            best_answer_states.append(TSP.State(0, best_answer.get_path()[0]))
            tsp.add_to_history(best_answer_states, best_answer.get_fitness())


        return best_answer.get_fitness()


