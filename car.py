from init import *
from random import *

class Car:
    def __init__(self, vertex):
        self.vertex = vertex
        self.s = 0.5
        self.v = 0
        self.acc = a_friction
        self.handlers = {}
        self.invincible = False

    def set_acc(self, mode: int):
        if mode == 0:
            self.acc = a_friction
        elif mode == 1:
            self.acc = a_gas
        else:
            self.acc = a_brake

    def update(self):
        self.v += dt * self.acc
        self.v = max(0, self.v)
        self.v = min(v_max, self.v)
        self.s += self.v * dt
        if self.s >= 1:

            if self.handlers:
                handlers_to_remove = []
                for handler in self.handlers.keys():
                    if self.vertex[0] == handler.vertex:
                        handler.car_crossed()
                        handlers_to_remove.append(handler)
                        self.invincible = False
                for handler in handlers_to_remove:
                    self.handlers.pop(handler)
            self.vertex = choice(vertices[self.vertex])
            self.s -= 1
