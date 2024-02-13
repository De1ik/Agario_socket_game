import pygame

from config import WIDTH_SCREEN, HEIGHT_SCREEN

class SetGrid:
    def __init__(self, screen):
        self.screen = screen
        self.start_size = 250
        self.size = 250
        self.x = -self.size
        self.y = -self.size
        self.colour = 'white'

    def upgrade_grid(self, scale, x_pos, y_pos):
        print(f'X POS: {-x_pos}')
        print(f'Y POS: {-y_pos}')
        print(f'size: {self.size}')
        print(f'scale: {scale}')
        self.size = self.start_size // scale
        self.x = -self.size + (-x_pos) % self.size
        self.y = -self.size + (-y_pos) % self.size
        # self.x = self.size + (-x_pos) % (self.size)
        # self.y = self.size + (-y_pos) % (self.size)
        pass

    def draw_grid(self):
        for i in range(WIDTH_SCREEN//self.size + 2):
            pygame.draw.line(self.screen, self.colour,
                             [self.x + i*self.size, 0],
                             [self.x + i*self.size, HEIGHT_SCREEN],
                             1)

        for i in range(HEIGHT_SCREEN // self.size + 2):
            pygame.draw.line(self.screen, self.colour,
                             [0, self.y + i * self.size],
                             [WIDTH_SCREEN, self.y + i * self.size],
                             1)
