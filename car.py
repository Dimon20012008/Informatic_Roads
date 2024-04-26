from init import *
from random import *


# Car class. Each frame every car receives its acceleration (set_acc) and updates by calculating its velocity and
# position within graph, updates cross handler system (look CrossHandler class in Simulator)
class Car:
    # init. Car has two types: normal and slower, which affects its max velocity and accelerations. Each car has its
    # position stored as a vertex and value s, responsible for position within tile; cross handlers for Simulator for
    # cross handler system.
    def __init__(self, vertex, type="normal"):
        self.vertex = vertex
        self.s = 0.5
        self.acc = a_friction
        self.handlers = {}
        self.type = type
        if self.type == "normal":
            self.v_max = v_max
            self.a_gas = a_gas
            self.a_brake = a_brake
        else:
            self.v_max = v_max_slower
            self.a_gas = a_gas_slower
            self.a_brake = a_brake_slower
        self.v = self.v_max

    # adapter for Simulator to change velocity (basically gas and brake pedal)
    def set_acc(self, mode: int):
        if mode == 0:
            self.acc = a_friction
        elif mode == 1:
            self.acc = self.a_gas
        else:
            self.acc = self.a_brake

    # update function. called each frame, and makes car to update its velocity and position, if moved onto the next
    # tile - picks next randomly and if it was on handler - updates it.
    def update(self):
        self.v += dt * self.acc
        self.v = max(0, self.v)
        self.v = min(self.v_max, self.v)
        self.s += self.v * dt

        if self.s >= 1:
            if self.handlers:
                handlers_to_work_with = []
                try:
                    for handler in self.handlers.keys():
                        if self.vertex[0] == handler.vertex or vertices[self.vertex][0][0] != handler.vertex:
                            handlers_to_work_with.append(handler)
                    for handler in handlers_to_work_with:
                        self.handlers.pop(handler)
                        handler.car_crossed(self)
                        if self.type == "slower":
                            print("crossed")
                except RuntimeError:
                    pass
            self.vertex = choice(vertices[self.vertex])
            self.s -= 1
