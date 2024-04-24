import numpy as np
import pygame

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
sector_rows, sector_cols = 4, 4
rows, cols = 4, 4
ROWS, COLS = sector_rows * rows, cols * sector_cols
map = np.ones((sector_rows * rows, cols * sector_cols), dtype=str)
vertices = {}
cars = []
a_friction = 0
a_gas = 30
a_brake = -60
v_max = 3
dt = 1 / 120
number_of_bots = 30
simulator = None
drawer = None

tile_width, tile_height = 50, 50

pygame.init()
screen = pygame.display.set_mode((tile_width * COLS, tile_height * ROWS))
clock = pygame.time.Clock()

