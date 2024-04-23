import init
from car import *
from random import *
from math import *


class Simulator:
    class CrossHandler:
        def __init__(self, pos):
            self.pos = pos
            self.queue = []
            self.current = None

        def car_crossed(self):
            current = None
            self.update()

        def update(self):
            if self.current is None and self.queue:
                self.current = self.queue.pop()
                self.current.cross_allowed = True
                self.current.handler = self

        def push(self, car: Car):
            self.queue.insert(0, car)

    def __init__(self):
        self.handlers = {}
        for y in range(ROWS):
            for x in range(COLS):
                if len(inv_tiles[map[y][x]]) > 2:  # this a cross
                    self.handlers[(y, x)] = self.CrossHandler((y, x))

    def get_acc_by_obstacles(self, car: Car):
        acc = 1
        vertices_to_check = []
        current = car.vertex
        brake_dist = car.v ** 2 / (2 * a_brake)
        brake_dist_max = v_max ** 2 / (2 * a_brake)
        cross = None

        for ver_i in range(ceil(brake_dist_max)):
            vertices_to_check.append(current)
            if len(vertices[current]) > 1:
                cross = current
                break
            current = vertices[current][0]
        for other_car in cars:
            if other_car.vertice in vertices_to_check:
                i = vertices_to_check.index(other_car.vertice)
                dist_between_cars = i - car.s + other_car.s
                if 0 < dist_between_cars < brake_dist:
                    return -1
                elif 0 < dist_between_cars < brake_dist_max:
                    acc = 0

        if cross is not None and not car.cross_allowed:
            dist_to_cross = vertices_to_check.index(cross) - car.s + 0.5
            if dist_to_cross < brake_dist:
                return -1
            elif dist_to_cross < brake_dist_max:
                return 0
        return acc

    def update(self):
        for car in cars:
            car.set_acc(self.get_acc_by_obstacles(car))
            if car.v == 0 and len(vertices[car.vertice]) > 1 and car.handler is None:
                self.handlers[vertices[car.vertex][0][0]].push(car)
                car.handler = self.handlers[vertices[car.vertex][0][0]]

