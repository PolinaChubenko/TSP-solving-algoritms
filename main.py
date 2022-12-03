from algorithms.ant import AntColony
from tsp import TSP
from algorithms.loop import LoopSolution
from typing import List


if __name__ == '__main__':
    n = int(input())

    cities: List[TSP.City] = []
    for i in range(n):
        id, x, y = input().split()
        cities.append(TSP.City(id, int(x), int(y)))

    tsp = TSP(cities)
    initial_state = TSP.State(1 << 0, 0)

    as_settings = AntColony.Settings()
    eas_settings = AntColony.Settings(elitist=3)
    mmas_settings = AntColony.Settings(infinity=1e5)
    ras_settings = AntColony.Settings(elitist=10)

    as_colony = AntColony(AntColony.Variation.ANT_SYSTEM, as_settings)
    eas_colony = AntColony(AntColony.Variation.ELITIST_ANT_SYSTEM, eas_settings)
    mmas_colony = AntColony(AntColony.Variation.MAXMIN_ANT_SYSTEM, mmas_settings)
    ras_colony = AntColony(AntColony.Variation.RANKBASED_ANT_SYSTEM, ras_settings)

    # print(tsp.cities_to_dict())
    path, dist = ras_colony.solve(initial_state, tsp.successors, tsp.goal, tsp.add_generation)
    print("Rank-based Ant System: ", [p.current_node for p in path], dist)
    # print(tsp.get_solution_in_generations())

    path, dist = eas_colony.solve(initial_state, tsp.successors, tsp.goal, tsp.add_generation)
    print("Elitist Ant System: ", [p.current_node for p in path], dist)

    path, dist = as_colony.solve(initial_state, tsp.successors, tsp.goal, tsp.add_generation)
    print("Ant System: ", [p.current_node for p in path], dist)

    path, dist = mmas_colony.solve(initial_state, tsp.successors, tsp.goal, tsp.add_generation)
    print("Max-Min Ant System: ", [p.current_node for p in path], dist)

    basic = LoopSolution(n)
    path, dist = basic.solve(initial_state.current_node, tsp.dist)
    print("Basic algo: ", path, dist)
