import numpy as np

tiles = {(): " ", (0, 1): "┗", (1, 2): "┏", (2, 3): "┓", (0, 3): "┛", (0, 2): "┃", (1, 3): "━", (0, 1, 2): "┣",
         (1, 2, 3): "┳", (0, 2, 3): "┫", (0, 1, 3): "┻", (0, 1, 2, 3): "╋"}
inv_tiles = {' ': (), '┗': (0, 1), '┏': (1, 2), '┓': (2, 3), '┛': (0, 3), '┃': (0, 2), '━': (1, 3), '┣': (0, 1, 2),
             '┳': (1, 2, 3), '┫': (0, 2, 3), '┻': (0, 1, 3), '╋': (0, 1, 2, 3)}

file_by_tile = {' ': '_.png', '┗': '01.png', '┏': '12.png', '┓': '23.png', '┛': '03.png', '┃': '02.png', '━': '13.png',
                '┣': '012.png', '┳': '123.png', '┫': '023.png', '┻': '013.png', '╋': '0123.png'}

functions_by_direction = {0: lambda cord: (cord[0] - 1, cord[1]), 1: lambda cord: (cord[0], cord[1] + 1),
                          2: lambda cord: (cord[0] + 1, cord[1]), 3: lambda cord: (cord[0], cord[1] - 1)}

sector_rows, sector_cols = 6, 6
rows, cols = 4, 4
ROWS, COLS = sector_rows * rows, cols * sector_cols
M = np.ones((sector_rows * rows, cols * sector_cols), dtype=str)
vertices = {}


