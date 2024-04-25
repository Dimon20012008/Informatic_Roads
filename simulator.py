import init
from car import *
from math import *


# singleton Simulator class is responsible for assigning acceleration values for cars by rules and updating them
class Simulator:
    # Cross system - the first car to arrive gets to cross, others wait
    # CrossHandler class, created for each cross. Has its own queue, current car which is moving, update process - if
    # there is no current car, then choose the first one from queue, if current car passed the cross - set it to
    # None. If all cars have stuck on the cross - select the first one and override all cross restriction,
    # so traffic jam goes out.
    class CrossHandler:
        # initialization. Each handler has its position, queue and current car
        def __init__(self, vertex):
            self.vertex = vertex
            self.queue = []
            self.current = None

        # since there is "slower" car, which has priority, this function returns the first car to be allowed to cross
        def get_first(self):
            for car in self.queue[::-1]:
                if car.type == "slower":
                    return car
            return self.queue[-1]

        # either car or handler detects, that car has passed the cross and sets current car to None and removes it
        # from the queue, then updates itself.
        def car_crossed(self):
            self.current = None
            if self.queue:
                self.queue.pop()
            self.update()

        # update process. checks if current car is None and if so - sets it to the first to cross. Also checks if
        # every car is stuck and pushes the first one to cross
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

        # adds car to the queue, sets itself for car as a current handler, and forbids to cross until further update
        def push(self, car: Car):
            self.queue.insert(0, car)
            car.handlers[self] = False

    # initialization for simulator. For each cross, asigns its own cross handler.
    def __init__(self):
        self.handlers = {}
        for y in range(ROWS):
            for x in range(COLS):
                if len(inv_tiles[map[y][x]]) > 2:  # this a cross
                    self.handlers[(y, x)] = self.CrossHandler((y, x))

    # calculates current acceleration for each car by checking, if there is forbidden cross or car within brake distance
    def get_acc_by_obstacles(self, car: Car):
        # calculations for distances
        acc = 1
        vertices_to_check = []
        current = car.vertex
        delta_car = 0.5
        if car.type == "slower":
            delta_car = 0.75
        brake_dist = abs(car.v ** 2 / (2 * car.a_brake)) + delta_car
        brake_dist_max = abs(car.v_max ** 2 / (2 * car.a_brake)) + delta_car

        # creates a list, where to possibly look for obstacles
        crosses = []
        for ver_i in range(ceil(brake_dist_max) + 1):
            if current not in vertices_to_check:
                vertices_to_check.append(current)
            if len(vertices[current]) > 1:
                crosses.append(vertices[current])
                if vertices[current] not in vertices_to_check:
                    vertices_to_check.append(vertices[current])
            current = vertices[current][0]

        # checks existence of cars on vertices within brake distance
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

        # checks existence of forbidden crosses on vertices within brake distance
        for cross in crosses:
            if not car.handlers.get(self.handlers[cross[0][0]], False):
                dist_to_cross = vertices_to_check.index(cross) - car.s + delta_car
                if dist_to_cross < brake_dist + delta_car:
                    return -1
                elif dist_to_cross < brake_dist_max + delta_car:
                    acc = 0
        return acc

    # for each car, sets it acceleration according to rules and adds it to respective cross handler when necessary.
    # Then updates every car and handler
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
