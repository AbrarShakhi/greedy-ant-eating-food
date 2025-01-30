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
    width, height = 800, 800
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Draw XY Tuples")
    background_color = (0, 0, 0)
    circle_color = (255, 255, 255)
    connected_line_color = (255, 0, 0)
    disconnected_line_color = (100, 10, 10)

    connected_points = []
    disconnected_points = []
    n = len(mat)
    for i in range(n):
        for j in range(n):
            ipos = info[i][3]
            jpos = info[j][3]
            if mat[i][j] != 0:
                connected_points.append(ipos)
                connected_points.append(jpos)
            else:
                disconnected_points.append(ipos)
                disconnected_points.append(jpos)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        screen.fill(background_color)

        if len(disconnected_points) >= 2:
            pygame.draw.lines(
                screen, disconnected_line_color, True, disconnected_points, 1
            )
        if len(connected_points) >= 2:
            pygame.draw.lines(screen, connected_line_color, True, connected_points, 2)

        for _, (_, _, _, (x, y)) in info.items():
            pygame.draw.circle(screen, circle_color, (x, y), 5)

        pygame.display.flip()


def main(data_dir="."):
    holes_info = load_hole_info_csv(path.join(data_dir, "info.csv"))
    mat = calc_paths(holes_info)
    display_graph(mat, holes_info)


if __name__ == "__main__":
    main("..")
    print()
