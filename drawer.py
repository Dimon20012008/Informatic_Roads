from init import *


class Drawer:
    def __init__(self):
        pass

    def draw(self):
        for y in range(ROWS):
            for x in range(COLS):
                file = file_by_tile[map[y][x]]
                img = pygame.image.load("images/tiles/" + file)
                img.convert()
                img = pygame.transform.scale(img, (tile_width, tile_height))
                rect = img.get_rect()
                rect.center = tile_width // 2 + x * tile_width, tile_height // 2 + y * tile_height
                screen.blit(img, rect)
                for car in cars:
                    car_y, car_x = car.vertex[0]
                    tile_type = car.vertex[1]
                    car_img_x, car_img_y = tile_width * (function_by_tile[tile_type](car.s)[0] + car_x), tile_height * (
                                function_by_tile[tile_type](car.s)[1] + car_y)
                    pygame.draw.circle(screen, "red", (car_img_x, car_img_y), 5)
                pygame.display.update()

