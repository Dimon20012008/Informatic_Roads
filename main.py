import generator
from simulator import *
from drawer import *

# generation
generator.generate_map()
generator.generate_vertices()
generator.generate_cars()

# initialisation of singletons
init.simulator = Simulator()
init.drawer = Drawer()

# main cycle, updates all cars and draws them
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    init.simulator.update()
    init.drawer.draw()
    pygame.display.flip()
    init.clock.tick(60)
