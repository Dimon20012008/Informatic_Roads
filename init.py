import numpy as np
import pygame

# various dictionaries for tile graph system. The system for tiles numbering: north is 0, then each one increases by
# 1 clockwise
tiles = {(): " ", (0, 1): "┗", (1, 2): "┏", (2, 3): "┓", (0, 3): "┛", (0, 2): "┃", (1, 3): "━", (0, 1, 2): "┣",
         (1, 2, 3): "┳", (0, 2, 3): "┫", (0, 1, 3): "┻", (0, 1, 2, 3): "╋"}
inv_tiles = {' ': (), '┗': (0, 1), '┏': (1, 2), '┓': (2, 3), '┛': (0, 3), '┃': (0, 2), '━': (1, 3), '┣': (0, 1, 2),
             '┳': (1, 2, 3), '┫': (0, 2, 3), '┻': (0, 1, 3), '╋': (0, 1, 2, 3)}
file_by_tile = {' ': '_.png', '┗': '01.png', '┏': '12.png', '┓': '23.png', '┛': '03.png', '┃': '02.png', '━': '13.png',
                '┣': '012.png', '┳': '123.png', '┫': '023.png', '┻': '013.png', '╋': '0123.png'}
functions_by_direction = {0: lambda cord: (cord[0] - 1, cord[1]), 1: lambda cord: (cord[0], cord[1] + 1),
                          2: lambda cord: (cord[0] + 1, cord[1]), 3: lambda cord: (cord[0], cord[1] - 1)}
function_by_tile = {(0, 1): lambda s: (0.375 + 0.625 * s, 0.625 * s),
                    (1, 0): lambda s: (1 - 0.375 * s, 0.375 - 0.375 * s),
                    (0, 2): lambda s: (0.375, s),
                    (2, 0): lambda s: (0.625, 1 - s),
                    (0, 3): lambda s: (0.375 - 0.375 * s, 0.375 * s),
                    (3, 0): lambda s: (0.625 * s, 0.625 - 0.625 * s),
                    (1, 2): lambda s: (1 - 0.625 * s, 0.375 + s * 0.625),
                    (2, 1): lambda s: (0.625 + s * 0.375, 1 - 0.375 * s),
                    (1, 3): lambda s: (1 - s, 0.375),
                    (3, 1): lambda s: (s, 0.625),
                    (2, 3): lambda s: (0.625 - s * 0.625, 1 - 0.625 * s),
                    (3, 2): lambda s: (s * 0.375, 0.625 + 0.375 * s)}

# map size and initialization
sector_rows, sector_cols = 4, 7
rows, cols = 4, 4
ROWS, COLS = sector_rows * rows, cols * sector_cols
tile_width, tile_height = 50, 50
map = np.ones((sector_rows * rows, cols * sector_cols), dtype=str)
vertices = {}

# cars properties. "Slower" car - has priority on crosses
cars = []

a_friction = -1
a_gas = 20
a_brake = -40
v_max = 3

a_gas_slower = 20
a_brake_slower = -60
v_max_slower = 1

number_of_bots = 30
number_of_slowers = 1

# singletons
simulator = None
drawer = None

# pygame init
dt = 1 / 120
pygame.init()
screen = pygame.display.set_mode((tile_width * COLS, tile_height * ROWS))
pygame.display.set_caption("Milky Way")
clock = pygame.time.Clock()
