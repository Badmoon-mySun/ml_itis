import copy
from itertools import cycle

import numpy as np
import pygame
import sys


MAX_DISTANCE = 50
MIN_NEIGHBORS = 3
BLACK_COLOR = 'black'
COLORS = ['red', 'blue', 'green', 'yellow', 'pink', 'orange', 'grey']
CIRCLE_RADIUS = 5


pygame.init()
screen = pygame.display.set_mode((1200, 800))
screen.fill(color='white')
pygame.display.update()


class Point:
    def __init__(self, x, y, color='black', cluster=None):
        self.x = x
        self.y = y
        self.color = color
        self.cluster = cluster

    def distance(self, point):
        return np.sqrt((self.x - point.x) ** 2 + (self.y - point.y) ** 2)

    def draw(self, screen):
        pygame.draw.circle(screen, self.cluster, (self.x, self.y), CIRCLE_RADIUS)


def get_neighbors(points, point, max_distance):
    return [p for p in points if point.distance(p) < max_distance]


def mark(points):
    points_copy = copy.deepcopy(points)
    colors_cycle = cycle(COLORS)

    for point in points_copy:
        if point.cluster:
            continue

        neighbors = get_neighbors(points_copy, point, MAX_DISTANCE)

        if len(neighbors) < MIN_NEIGHBORS:
            point.cluster = BLACK_COLOR
            continue

        color = next(colors_cycle)
        point.cluster = color

        for neighbor in neighbors:
            if neighbor.cluster == BLACK_COLOR:
                neighbor.cluster = color
            elif neighbor.cluster is not None:
                continue

            neighbor.cluster = color
            new_neighbors = get_neighbors(points_copy, neighbor, MAX_DISTANCE)

            if len(new_neighbors) >= MIN_NEIGHBORS:
                neighbors += [n for n in new_neighbors if n not in neighbors]

    return points_copy


if __name__ == '__main__':
    points = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pygame.draw.circle(screen, color='black', center=event.pos, radius=CIRCLE_RADIUS)
                points.append(Point(*event.pos))
                pygame.display.update()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                new_points = mark(points)
                for point in new_points:
                    point.draw(screen)
                pygame.display.update()
            if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
