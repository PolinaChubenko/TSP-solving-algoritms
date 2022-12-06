from scipy.stats import randint
import os.path


if __name__ == '__main__':
    n_cities = int(input("Number of cities: "))
    low_coord = int(input("Lowest coord: "))
    high_coord = int(input("Highest coord: "))

    x_coord_list = randint.rvs(low_coord, high_coord, size=n_cities)
    y_coord_list = randint.rvs(low_coord, high_coord, size=n_cities)

    i = 1
    file_name = f"{n_cities}cities_{i}.txt"
    while os.path.exists(file_name):
        i += 1

    f = open(file_name, 'w', encoding="utf-8")

    for i in range(n_cities):
        f.write(f"{i + 1} {x_coord_list[i]} {y_coord_list[i]}\n")
