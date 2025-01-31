from src.mst import make_mst

from sys import exit
from csv import reader
from os import path
from math import sqrt
import numpy as np
import pygame


def load_hole_info_csv(filename) -> dict:
    holes = {}

    with open(filename, mode="r") as file:
        csv_reader = reader(file)
        next(csv_reader)

        for row in csv_reader:
            hole_number = int(row[0])
            reveal = int(row[1])
            finish = int(row[2])
            flag_val = int(row[3])
            pos = (int(row[4]), int(row[5]))
            holes[hole_number] = (reveal, finish, flag_val, pos)

    return holes


def calc_paths(info):
    n = len(info)
    for i, _ in info.items():
        n = max(i, n)

    adjmat = np.zeros((n, n), dtype=int)
    for i in range(n):
        for j in range(n):
            ipos = info[i][3]
            jpos = info[j][3]
            iX, iY = ipos
            jX, jY = jpos
            distance = int(sqrt((iX - jX) ** 2 + (iY - jY) ** 2))
            adjmat[i][j] = distance

    return adjmat


def display_graph(mat, info) -> None:
    pygame.init()
    clock = pygame.time.Clock()

    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Draw XY Tuples")
    background_color = (0, 0, 0)
    circle_color = (255, 255, 255)
    connected_line_color = (255, 100, 0)
    disconnected_line_color = (40, 0, 0)

    connected_points = []
    disconnected_points = []
    n = len(mat)
    for i in range(n):
        for j in range(i, n):
            ipos = info[i][3]
            jpos = info[j][3]
            if mat[i][j] != 0:
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
            pygame.draw.line(screen, disconnected_line_color, a, b, 1)
        for a, b in connected_points:
            pygame.draw.line(screen, connected_line_color, a, b, 1)

        for _, (_, _, _, pos) in info.items():
            pygame.draw.circle(screen, circle_color, pos, 5)

        clock.tick(12)
        pygame.display.flip()


def main(data_dir="."):
    holes_info = load_hole_info_csv(path.join(data_dir, "info.csv"))
    adjmat = calc_paths(holes_info)

    display_graph(adjmat, holes_info)

    mst_adjmat = make_mst(adjmat)
    print(mst_adjmat)

    display_graph(mst_adjmat, holes_info)


if __name__ == "__main__":
    main("..")
    print()
