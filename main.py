import init
import generator
from simulator import *
from drawer import *

generator.generate_map()
generator.generate_vertices()
generator.generate_cars()

init.simulator = Simulator()
init.drawer = Drawer()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    init.simulator.update()
    init.drawer.draw()
    pygame.display.flip()
    init.clock.tick(60)
