from random import *
from init import *
from car import Car


def get_value(y, x):
    if 0 <= y < ROWS and 0 <= x < COLS:
        return map[y, x]
    return " "


def generate_map():
    def rect(point1, point2):

        map[min(point1[0], point2[0]):min(point1[0], point2[0]) + 1,
        min(point1[1], point2[1]):max(point1[1], point2[1])] = "▢"
        map[max(point1[0], point2[0]):max(point1[0], point2[0]) + 1,
        min(point1[1], point2[1]):max(point1[1], point2[1])] = "▢"
        map[min(point1[0], point2[0]):max(point1[0], point2[0]),
        min(point1[1], point2[1]):min(point1[1], point2[1]) + 1] = "▢"
        map[min(point1[0], point2[0]):max(point1[0], point2[0]) + 1,
        max(point1[1], point2[1]):max(point1[1], point2[1]) + 1] = "▢"

    def fill_rect(points):
        point1, point2 = points
        map[min(point1[0], point2[0]) + 1:max(point1[0], point2[0]),
        min(point1[1], point2[1]) + 1:max(point1[1], point2[1])] = "▦"

    map[:, :] = "▦"
    # (y,x)
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

    def is_road(t):
        if t == "▦" or t == " ":
            return False
        return True

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

    fill_rect(points[randint(0, 3)])

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


# for two_side: 0 clock wise, 1 counter clock wise. For others:
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


def generate_cars():
    all_starts = list(vertices.keys())
    shuffle(all_starts)

    starts_slower = all_starts[:number_of_slowers]
    starts = all_starts[number_of_slowers:number_of_bots]

    for start_slower in starts_slower:
        cars.append(Car(start_slower, type="slower"))

    for start in starts:
        cars.append(Car(start))

