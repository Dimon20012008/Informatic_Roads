from init import *


class Drawer:
    def __init__(self):
        self.pic_by_tile = {}
        for tile in file_by_tile.keys():
            file = file_by_tile[tile]
            img = pygame.image.load("images/tiles/" + file)
            img.convert()
            img = pygame.transform.scale(img, (tile_width, tile_height))
            self.pic_by_tile[tile] = img
        car_img = pygame.image.load('images/car.png')
        car_img.convert()
        car_img = pygame.transform.scale(car_img, (tile_width // 8, tile_height // 8))
        self.car_img = car_img

    def draw(self):
        for y in range(ROWS):
            for x in range(COLS):
                img = self.pic_by_tile[map[y][x]]
                rect = img.get_rect()
                rect.center = tile_width // 2 + x * tile_width, tile_height // 2 + y * tile_height
                screen.blit(img, rect)
        for car in cars:
            car_y, car_x = car.vertex[0]
            tile_type = car.vertex[1]
            car_img_x, car_img_y = tile_width * (function_by_tile[tile_type](car.s)[0] + car_x), tile_height * (
                    function_by_tile[tile_type](car.s)[1] + car_y)
            img = self.car_img
            rect = img.get_rect()
            rect.center = car_img_x, car_img_y
            screen.blit(img, rect)

        pygame.display.update()

