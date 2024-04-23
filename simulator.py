import init
from car import *
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

        def push(self, car: Car):
            self.queue.insert(0, car)