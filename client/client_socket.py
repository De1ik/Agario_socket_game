from math import hypot
import socket
import pygame
import ctypes

from utilites.receive_data_type import get_field_cond
from utilites.draw import draw_opponents
from grid.game_grid import SetGrid
from config import *


# connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
client_socket.connect(('localhost', 10000))

PLAYER_COLOUR, PLAYER_RADIUS = (client_socket.recv(256).decode()).split(' ')


pygame.init()
clock = pygame.time.Clock()




# Получение разрешения экрана пользователя
# user32 = ctypes.windll.user32
# user32.SetProcessDPIAware()
# screen_width = user32.GetSystemMetrics(0)
# screen_height = user32.GetSystemMetrics(1)

# create a game window
screen = pygame.display.set_mode((WIDTH_SCREEN, HEIGHT_SCREEN))
pygame.display.set_caption('Delik Agario Game')



grid = SetGrid(screen)


problems = 0
vector = old_vector = (WIDTH_SCREEN//2, HEIGHT_SCREEN//2)
running = True
while running:
    clock.tick(FPS)

    # receive player command
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check player mouse position
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = (pos[0]-WIDTH_SCREEN//2, pos[1]-HEIGHT_SCREEN//2)
        if hypot(vector[0], vector[1]) <= 50:
            vector = (0,0)



    # send player command
    try:
        if vector != old_vector:
            message = f'<{str(vector[0])}, {str(vector[1])}>'
            old_vector = vector
            client_socket.send(message.encode())
    except Exception as ex:
        print(ex)


    # receive new field condition
    try:
        new_field = client_socket.recv(16384)
        new_field = new_field.decode()
        if new_field != '':
            new_field = get_field_cond(new_field)
            draw_opponents(new_field, screen, PLAYER_COLOUR, grid)
            pygame.display.update()
    except:
        break




pygame.quit()

