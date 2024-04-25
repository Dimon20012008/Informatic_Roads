import init
from car import *
from random import *
from math import *


class Simulator:
    class CrossHandler:
        def __init__(self, vertex):
            self.vertex = vertex
            self.queue = []
            self.current = None

        def get_first(self):
            for car in self.queue[::-1]:
                if car.type == "slower":
                    return car
            return self.queue[-1]

        def car_crossed(self):
            self.current = None
            if self.queue:
                self.queue.pop()
            self.update()

        def update(self):
            if self.current is None and self.queue:
                self.current = self.get_first()
                self.current.handlers[self] = True
            stuck = True

            for car in self.queue:
                if not (car.v == 0 and car.acc <= 0):
                    stuck = False
                    break
                if init.simulator is not None:
                    if init.simulator.get_acc_by_obstacles(car) >= 0:
                        stuck = False
                        break

            if stuck and self.queue:
                first_car = self.get_first()
                for handler in first_car.handlers.keys():
                    first_car.handlers[handler] = True
                first_car.set_acc(1)
                first_car.v = v_max
                first_car.update()

        def push(self, car: Car):
            self.queue.insert(0, car)
            car.handlers[self] = False

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
        delta_car = 0.5
        if car.type == "slower":
            delta_car = 0.75
        brake_dist = abs(car.v ** 2 / (2 * car.a_brake)) + delta_car
        brake_dist_max = abs(car.v_max ** 2 / (2 * car.a_brake)) + delta_car

        crosses = []
        for ver_i in range(ceil(brake_dist_max) + 1):
            if current not in vertices_to_check:
                vertices_to_check.append(current)
            if len(vertices[current]) > 1:
                crosses.append(vertices[current])
                if vertices[current] not in vertices_to_check:
                    vertices_to_check.append(vertices[current])
            current = vertices[current][0]

        for other_car in cars:
            if other_car == car:
                continue
            if other_car.vertex in vertices_to_check:

                i = vertices_to_check.index(other_car.vertex)
                dist_between_cars = i - car.s + other_car.s
                if 0 < dist_between_cars < brake_dist:
                    return -1
                elif 0 < dist_between_cars < brake_dist_max:
                    acc = 0

        for cross in crosses:
            if not car.handlers.get(self.handlers[cross[0][0]], False):
                dist_to_cross = vertices_to_check.index(cross) - car.s + delta_car
                if dist_to_cross < brake_dist + delta_car:
                    return -1
                elif dist_to_cross < brake_dist_max + delta_car:
                    acc = 0
        return acc

    def update(self):
        for car in cars:
            car.set_acc(self.get_acc_by_obstacles(car))

            if car.v == 0 and len(vertices[car.vertex]) > 1 and not car.handlers.get(
                    self.handlers[vertices[car.vertex][0][0]], False):
                if car not in self.handlers[vertices[car.vertex][0][0]].queue:
                    self.handlers[vertices[car.vertex][0][0]].push(car)
            car.update()
        for handler_key in self.handlers.keys():
            self.handlers[handler_key].update()
