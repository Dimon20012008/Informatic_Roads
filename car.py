from init import *
from random import *


class Car:
    def __init__(self, vertex, type="normal"):
        self.vertex = vertex
        self.s = 0.5

        self.acc = a_friction
        self.handlers = {}
        self.invincible = False
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

    def set_acc(self, mode: int):
        if mode == 0:
            self.acc = a_friction
        elif mode == 1:
            self.acc = self.a_gas
        else:
            self.acc = self.a_brake

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
                        handler.car_crossed()

                except RuntimeError:
                    pass
            self.vertex = choice(vertices[self.vertex])
            self.s -= 1
