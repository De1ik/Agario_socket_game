from random import randint, choice

from server_config import WIDTH_WINDOW, HEIGHT_WINDOW, PLAYER_COLOURS, FOODS_RADIUS, WIDTH_WINDOW, HEIGHT_WINDOW


class Food:
    def __init__(self, r, x, y, c):
        self.radius = FOODS_RADIUS
        self.x = randint(0, WIDTH_WINDOW)
        self.y = randint(0, HEIGHT_WINDOW)
        self.colour = choice(PLAYER_COLOURS)

    def reset(self, r=None, x=None, y=None):
        self.radius = FOODS_RADIUS
        self.x = randint(0, WIDTH_WINDOW)
        self.y = randint(0, HEIGHT_WINDOW)