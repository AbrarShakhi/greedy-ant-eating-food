from sys import exit, argv
from csv import reader
from os import path
from math import sqrt

try:
    import pygame
except:
    print("pygame is not installed.")
    print("please install pygame.")
    exit(1)
try:
    import numpy as np
except:
    print("numpy is not installed.")
    print("please install numpy.")
    exit(1)


# error --------------------------------------------------
def show_input_file_error(filename):
    print("Unable to open file ", filename, " or file don't exists")
    print("Use -p [path] set the path")
    print("exemple:")
    print('python main.py -p "info.csv"')
    exit()


# minimam spanning tree ---------------------------------
class DisjointSetUnion:
    def __init__(self):
        self.__set = {}
        self.__size = {}

    def make_set(self, item):
        self.__set[item] = item
        self.__size[item] = 1

    def find_set(self, item):
        if self.__set[item] == item:
            return item
        self.__set[item] = self.find_set(self.__set[item])
        return self.__set[item]

    def union_set(self, item1, item2):
        item1 = self.find_set(item1)
        item2 = self.find_set(item2)
        if item1 != item2:
            if self.__size[item1] < self.__size[item2]:
                self.__set[item1] = item2
                self.__size[item2] += self.__size[item1]
            else:
                self.__set[item2] = item1
                self.__size[item1] += self.__size[item2]


def make_mst(adjmat):
    n = len(adjmat)
    mst_adjmat = np.zeros((n, n), dtype=int)
    edges = []

    for i in range(n):
        for j in range(i, n):
            edges.append((int(adjmat[i][j]), (i, j)))

    edges = sorted(edges, key=lambda based_on: based_on[0])

    dsu = DisjointSetUnion()
    for _, (i, j) in edges:
        dsu.make_set(i)
        if i != j:
            dsu.make_set(j)

    for wight, (i, j) in edges:
        iclan = dsu.find_set(i)
        jclan = dsu.find_set(j)
        if iclan != jclan:
            mst_adjmat[i][j] = wight
            mst_adjmat[j][i] = wight
            dsu.union_set(i, j)

    return mst_adjmat


# input ----------------------------------------
def load_hole_info_csv(filename):
    foods = {}

    try:
        with open(filename, mode="r") as file:
            csv_reader = reader(file)
            next(csv_reader)

            for row in csv_reader:
                food_number = int(row[0])
                appear = int(row[1])
                waste = int(row[2])
                food_val = int(row[3])
                pos = (int(row[4]), int(row[5]))
                foods[food_number] = (appear, waste, food_val, pos)
    except FileNotFoundError or FileExistsError:
        show_input_file_error(filename)
    return foods


def calc_paths(info):
    n = len(info)
    for i, _ in info.items():
        n = max(i, n)

    adjmat = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(i, n):
            ipos = info[i][3]
            jpos = info[j][3]
            iX, iY = ipos
            jX, jY = jpos
            distance = int(sqrt((iX - jX) ** 2 + (iY - jY) ** 2))
            adjmat[i][j] = distance
            adjmat[j][i] = distance

    return adjmat


# pygame -----------------------------------------------
def display_graph(
    matrix,
    info,
    highlight=[],
    window_title="food scattered path",
    width=1200,
    height=800,
) -> None:
    window_size = (width, height)

    pygame.init()
    clock = pygame.time.Clock()

    background_color = (0, 0, 0)
    circle_color = (255, 255, 255)
    connected_line_color = (255, 0, 0)
    disconnected_line_color = (50, 0, 0)
    highlighted_circle_color = (0, 255, 0)

    connected_points = []
    disconnected_points = []

    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(window_title)

    n = len(matrix)
    for i in range(n):
        for j in range(i, n):
            ipos = info[i][3]
            jpos = info[j][3]

            if matrix[i][j] != 0:
                connected_points.append((ipos, jpos))
            else:
                disconnected_points.append((ipos, jpos))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(background_color)

        for a, b in disconnected_points:
            pygame.draw.line(screen, disconnected_line_color, a, b)

        for a, b in connected_points:
            pygame.draw.line(screen, connected_line_color, a, b)

        for _, (_, _, val, pos) in info.items():
            pygame.draw.circle(screen, circle_color, pos, val)

        for i in highlight:
            _, _, val, pos = info[i]
            pygame.draw.circle(screen, highlighted_circle_color, pos, val)

        clock.tick(11)
        pygame.display.flip()


# activity selection
def select_max_foods(info):
    n = len(info)
    for i, _ in info.items():
        n = max(i, n)

    info_list = [None] * n
    for i, tup in info.items():
        info_list[i] = (i, tup[0], tup[1])

    info_list = sorted(info_list, key=lambda based_on: based_on[2])

    i = 0
    selected_food_no = [info_list[0][0]]
    for j in range(1, n):
        if info_list[j][1] >= info_list[i][2]:
            selected_food_no.append(info_list[j][0])
            i = j

    return selected_food_no


# 0/1 knapsack ----------------------------------
def maximum_test_in_time(W, holes_info, selection):
    holes = []
    for i in selection:
        starttime, endtime, value, _ = holes_info[i]
        duration = endtime - starttime
        if duration < 0:
            print("there is error on input")
            print("finish time > staring time")
            exit(-1)
        holes.append((value / duration, duration, value))

    holes = sorted(holes, reverse=True, key=lambda x: x[0])

    total_value = 0
    remaining_weight = W

    for value_per_time, duration, value in holes:
        if remaining_weight == 0:
            break

        if duration <= remaining_weight:
            total_value += value
            remaining_weight -= duration
        else:
            total_value += value_per_time * remaining_weight
            remaining_weight = 0

    return total_value


# main ----------------------------------------------------
def main(input_filepath):
    foods_info = load_hole_info_csv(input_filepath)
    foodpath_adjmat = calc_paths(foods_info)

    display_graph(matrix=foodpath_adjmat, info=foods_info)

    mst_foodpath_adjmat = make_mst(foodpath_adjmat)

    display_graph(
        matrix=mst_foodpath_adjmat,
        info=foods_info,
        window_title="food scattered path with minimum distance (minimum spanning tree)",
    )

    selected_food_no = select_max_foods(foods_info)
    display_graph(
        matrix=mst_foodpath_adjmat,
        info=foods_info,
        highlight=selected_food_no,
        window_title="maximum food selected (greens)",
    )

    maximum_time_to_eat = 100  # totl weight of frk
    max_test = maximum_test_in_time(maximum_time_to_eat, foods_info, selected_food_no)
    print(max_test)


if __name__ == "__main__":
    input_filepath = path.join(".", "info.csv")
    for i, arg in enumerate(argv):
        if arg == "-p" or arg == "--path":
            try:
                input_filepath = argv[i + 1]
            except:
                print("filepath required")
                show_input_file_error(None)
                exit()
            break

    main(input_filepath)
