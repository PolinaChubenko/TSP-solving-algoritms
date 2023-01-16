from algorithms.ant import AntColony
from tsp import TSP
from algorithms.loop import LoopSolution
from typing import List

from algorithms.genetic.genetic import GeneticAlgorithm
from algorithms.genetic.creation import RandomCreation
from algorithms.genetic.selection import TournamentSelection, RouletteSelection, RankSelection
from algorithms.genetic.crossover import InbreedingParentGenerator, OutbreedingParentGenerator, PanmixiaParentGenerator, OrderCrossover, EdgeRecombinationCrossover
from algorithms.genetic.mutation import SwapMutation, ScrambleMutation, TwoOptMutation

def choose_ants(tsp: TSP):
    print("""Типы алгоритмов:
        1 - Ant System
        2 - Elitist Ant System
        3 - Max-Min Ant System
        4 - Rank-based Ant System""")

    type = int(input("Мой выбор: "))

    if type == 1:
        as_settings = AntColony.Settings()
        as_colony = AntColony(AntColony.Variation.ANT_SYSTEM, as_settings)
        dist = as_colony.solve(tsp, logging=False)
        print("Ant System: ", dist)

    elif type == 2:
        eas_settings = AntColony.Settings(elitist=3)
        eas_colony = AntColony(AntColony.Variation.ELITIST_ANT_SYSTEM, eas_settings)
        dist = eas_colony.solve(tsp, logging=False)
        print("Elitist Ant System: ", dist)

    elif type == 3:
        mmas_settings = AntColony.Settings(infinity=1e5, rho=0.02)
        mmas_colony = AntColony(AntColony.Variation.MAXMIN_ANT_SYSTEM, mmas_settings)
        dist = mmas_colony.solve(tsp, logging=False)
        print("Max-Min Ant System: ", dist)

    elif type == 4:
        ras_settings = AntColony.Settings(elitist=6, rho=0.1)
        ras_colony = AntColony(AntColony.Variation.RANKBASED_ANT_SYSTEM, ras_settings)
        dist = ras_colony.solve(tsp, logging=False)
        print("Rank-based Ant System: ", dist, tsp.solution)



def choose_genetic(tsp: TSP):
    print("""Selection:
            1 - лучшие параметры
            2 - задать вручную""")

    type = int(input("Мой выбор: "))

    if type == 1:
        population_size = 1000
        iterations = 500
        survived = 0.6
        mutated = 0.3
        selection = RouletteSelection(survived)
        parent_generator = InbreedingParentGenerator()
        crossover = EdgeRecombinationCrossover()
        mutation = TwoOptMutation(mutated)
    else:
        population_size = int(input("Размер популяции: "))
        iterations = int(input("Количество итераций: "))
        survived = float(input("Доля выживающих особей: "))
        mutated = float(input("Доля мутирующих особей: "))

        print("""Selection:
                1 - Tournament Selection
                2 - Roulette Wheel Selection
                3 - Rank Selection""")

        type = int(input("Мой выбор: "))

        if type == 1:
            selection = TournamentSelection(survived)
        elif type == 2:
            selection = RouletteSelection(survived)
        elif type == 3:
            selection = RankSelection(survived)

        print("""Parent Generator:
                    1 - Inbreeding
                    2 - Outbreeding
                    3 - Panmixia""")

        type = int(input("Мой выбор: "))

        if type == 1:
            parent_generator = InbreedingParentGenerator()
        elif type == 2:
            parent_generator = OutbreedingParentGenerator()
        elif type == 3:
            parent_generator = PanmixiaParentGenerator()

        print("""Crossover:
                    1 - Order
                    2 - Edge Recombination""")

        type = int(input("Мой выбор: "))

        if type == 1:
            crossover = OrderCrossover()
        elif type == 2:
            crossover = EdgeRecombinationCrossover()

        print("""Mutation:
                    1 - Swap
                    2 - Scramble
                    3 - 2-opt""")

        type = int(input("Мой выбор: "))

        if type == 1:
            mutation = SwapMutation(mutated)
        elif type == 2:
            mutation = ScrambleMutation(mutated)
        elif type == 3:
            mutation = TwoOptMutation(mutated)

    ga_settings = GeneticAlgorithm.Settings(survived=survived, mutated=mutated, iterations=iterations,
                                            creation=RandomCreation(population_size),
                                            selection=selection,
                                            parent_generator=parent_generator,
                                            crossover=crossover,
                                            mutation=mutation)
    ga = GeneticAlgorithm(ga_settings)
    dist = ga.solve(tsp)
    print("Генетический алгоритм: ", dist)


if __name__ == '__main__':
    n = int(input("Количество городов: "))

    print('Введите города в формате <id x y>')
    cities: List[TSP.City] = []
    for i in range(n):
        id, x, y = input().split()
        cities.append(TSP.City(id, int(x), int(y)))

    tsp = TSP(cities)

    print("""Типы алгоритмов:
        0 - обычный перебор
        1 - Ant System
        2 - Генетический алгоритм""")

    type = int(input("Мой выбор: "))

    if type == 0:
        basic = LoopSolution(n)
        initial_state = TSP.State(1 << 0, 0)
        dist = basic.solve(initial_state.current_node, tsp.dist)
        print("Basic algo: ", dist)
    elif type == 1:
        choose_ants(tsp)
    elif type == 2:
        choose_genetic(tsp)




    tsp.clear_answer()
