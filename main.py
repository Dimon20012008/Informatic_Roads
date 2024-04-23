from init import *
import generator
from simulator import *
from drawer import *

generator.generate_map()
generator.generate_vertices()
generator.generate_cars()

simulator = Simulator()

drawer = Drawer()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    simulator.update()
    drawer.draw()
    pygame.display.flip()
    clock.tick(60)