import pygame

from config import WIDTH_SCREEN, HEIGHT_SCREEN


def draw_opponents(data, screen, player_colour, grid):
        screen.fill('gray28')
        dt = data.split(',')
        player_radius = int(dt[0])
        x_pos = int(dt[1])
        y_pos = int(dt[2])
        scale = int(dt[3])
        grid.upgrade_grid(scale, x_pos, y_pos)
        grid.draw_grid()
        if dt[4]:
            for opponent in dt[4:]:
                x, y, r, col = opponent.split(' ')
                x = (WIDTH_SCREEN//2) + int(x)
                y = (HEIGHT_SCREEN//2) + int(y)
                pygame.draw.circle(screen, col, (x, y), int(r))

        pygame.draw.circle(screen, player_colour, (WIDTH_SCREEN // 2, HEIGHT_SCREEN // 2), player_radius)
        pygame.display.update()
