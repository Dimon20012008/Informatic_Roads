from random import *
from init import *
from car import Car


# simple function to avoid checking each time, whether requested value is within the map
def get_value(y, x):
    if 0 <= y < ROWS and 0 <= x < COLS:
        return map[y, x]
    return " "


# generates a map, based on its size. Generation process is simple - there are generated 4 rectangles such that they
# cover most of the map (which is done by spliting the whole map into 16 sectors and placing each rectangle vertice
# in different one, so rectangles are big), these cells will be road tiles. Then each tile by looking at its
# neighbours decides its type
def generate_map():
    # generate a rectangle on the map based on two points. It doesn't care about points position relative to each
    # other (whose coordinates are bigger), if their x and y are different - that's sufficient.
    def rect(point1, point2):

        map[min(point1[0], point2[0]):min(point1[0], point2[0]) + 1,
        min(point1[1], point2[1]):max(point1[1], point2[1])] = "▢"
        map[max(point1[0], point2[0]):max(point1[0], point2[0]) + 1,
        min(point1[1], point2[1]):max(point1[1], point2[1])] = "▢"
        map[min(point1[0], point2[0]):max(point1[0], point2[0]),
        min(point1[1], point2[1]):min(point1[1], point2[1]) + 1] = "▢"
        map[min(point1[0], point2[0]):max(point1[0], point2[0]) + 1,
        max(point1[1], point2[1]):max(point1[1], point2[1]) + 1] = "▢"

    # called once for a random rectangle, fills everything within this rectangle.
    def fill_rect(points):
        point1, point2 = points
        map[min(point1[0], point2[0]) + 1:max(point1[0], point2[0]),
        min(point1[1], point2[1]) + 1:max(point1[1], point2[1])] = "▦"

    # map with road placement generation process (map now has two types of elements - there will be road, there won't
    # be road)
    map[:, :] = "▦"
    sectors = [((0, 0), (2, 2)), ((0, 3), (2, 1)), ((3, 0), (1, 2)), ((1, 1), (3, 3))]
    points = []
    for road in sectors:
        point1 = (randint(road[0][0] * sector_rows, (road[0][0] + 1) * sector_rows - 1)), randint(
            road[0][1] * sector_cols,
            (road[0][
                 1] + 1) * sector_cols - 1)
        point2 = (randint(road[1][0] * sector_rows, (road[1][0] + 1) * sector_rows - 1)), randint(
            road[1][1] * sector_cols,
            (road[1][
                 1] + 1) * sector_cols - 1)
        rect(point1, point2)
        points.append((point1, point2))
    fill_rect(points[randint(0, 3)])

    # checks if current tile is road, necessary since during update some tiles will turn into spaces (for printing)
    def is_road(t):
        if t == "▦" or t == " ":
            return False
        return True

    # return a tuple of neighbours of current tile. the tuple is a key for dictionaries.
    def get_road_neighbours(y, x):
        l = []
        if is_road(get_value(y - 1, x)):
            l.append(0)
        if is_road(get_value(y, x + 1)):
            l.append(1)
        if is_road(get_value(y + 1, x)):
            l.append(2)
        if is_road(get_value(y, x - 1)):
            l.append(3)

        if get_value(y, x) != "▦":
            return tuple(l)
        return ()

    # tile specification process. Also, if there are two or three parallel roads, they are converted from parallel
    # T-turns to two parallel roads, because it looks nicer
    for y in range(rows * sector_rows):
        for x in range(cols * sector_cols):
            map[y][x] = tiles[get_road_neighbours(y, x)]
            if get_value(y - 1, x) == tiles[(1, 2, 3)] and get_value(y, x) == tiles[(0, 1, 3)]:
                map[y][x] = tiles[(1, 3)]
                map[y - 1][x] = tiles[(1, 3)]
            elif get_value(y, x - 1) == tiles[(0, 1, 2)] and get_value(y, x) == tiles[(0, 2, 3)]:
                map[y][x] = tiles[(0, 2)]
                map[y][x - 1] = tiles[(0, 2)]
            elif get_value(y, x) == tiles[(0, 1, 3)] and get_value(y - 1, x) == tiles[(0, 1, 2, 3)] and get_value(y - 2,
                                                                                                                  x) == \
                    tiles[(1, 2, 3)]:
                map[y - 1][x] = tiles[(1, 3)]
                map[y - 2][x] = tiles[(1, 3)]
                map[y][x] = tiles[(1, 3)]
            elif get_value(y, x) == tiles[(0, 2, 3)] and get_value(y, x - 1) == tiles[(0, 1, 2, 3)] and get_value(y,
                                                                                                                  x - 2) == \
                    tiles[(0, 1, 2)]:
                map[y][x] = tiles[(0, 2)]
                map[y][x - 1] = tiles[(0, 2)]
                map[y][x - 2] = tiles[(0, 2)]


# process of generating the graph. For each end of tile, all possible pairs of connected roads are generated and
# added as adjacency list. Explanation of graph system: each tile has several vertices, each one responsible for
# certain part of the road (e.g., in (0,2) there is right and left side. Left one is connected to the bottom tile,
# right - top tile), then all possible pairs of two consecutive vertices are generated and put into adjacency list
def generate_vertices():
    for y in range(ROWS):
        for x in range(COLS):
            tile = inv_tiles[map[y][x]]
            for direction in tile:
                for i in range(4):
                    if direction == i:
                        next_tile = inv_tiles[get_value(functions_by_direction[direction]((y, x))[0],
                                                        functions_by_direction[direction]((y, x))[1])]
                        neighbours = []
                        for neighbour in next_tile:
                            if neighbour == (direction + 2) % 4:
                                continue
                            neighbours.append(
                                (functions_by_direction[direction]((y, x)), ((direction + 2) % 4, neighbour)))
                        for start in tile:
                            if start != direction:
                                vertices[((y, x), (start, direction))] = neighbours


# picks random tiles and puts cars on them, considering amount of "slowers" and overall.
def generate_cars():
    all_starts = list(vertices.keys())
    shuffle(all_starts)

    starts_slower = all_starts[:number_of_slowers]
    starts = all_starts[number_of_slowers:number_of_bots]

    for start_slower in starts_slower:
        cars.append(Car(start_slower, type="slower"))

    for start in starts:
        cars.append(Car(start))
