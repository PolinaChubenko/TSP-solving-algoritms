from algorithms.ant import AntColony
from tsp import TSP
from algorithms.loop import LoopSolution
from typing import List


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
    2 - Elitist Ant System
    3 - Max-Min Ant System
    4 - Rank-based Ant System""")

    type = int(input("Мой выбор: "))

    if type == 0:
        basic = LoopSolution(n)
        initial_state = TSP.State(1 << 0, 0)
        dist = basic.solve(initial_state.current_node, tsp.dist)
        print("Basic algo: ", dist)

    elif type == 1:
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

    tsp.clear_answer()


