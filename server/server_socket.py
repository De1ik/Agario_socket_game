import pygame
from random import randint, choice

from server_config import *
from set_socket import main_socket
from utilites.recieve_data import get_correct_type
from utilites.reset_players_bots import check_rad_food
from utilites.set_player_screen import check_visibility, check_eating
from player.player_class import PlayerSet
from foods.agario_food import Food


server_running = False


# init pygame and draw pygame screen
pygame.init()
if not server_running:
    screen = pygame.display.set_mode((WIDTH_SERVER_WIND, HEIGHT_SERVER_WIND))
clock = pygame.time.Clock()


foods = [
    Food(r=FOODS_RADIUS,
         x=randint(0, WIDTH_WINDOW),
         y=randint(0, HEIGHT_WINDOW),
         c=choice(PLAYER_COLOURS))
    for i in range(FOODS_QUANTITY)
]

all_players = [
    PlayerSet(x_pos=randint(0, WIDTH_WINDOW),
              y_pos=randint(0, HEIGHT_WINDOW),
              radius=randint(25, 100),
              colour=choice(PLAYER_COLOURS))
    for j in range(BOTS_QUANTITY)
]

running = True
tick = 249
scale_click = 0
while running:
    clock.tick(FPS)
    tick += 1

    # check quite-event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break


    # add new user and reconnect them to the new personal port
    try:
        if tick % 200 == 0:
            new_socket, addr = main_socket.accept()
            new_socket.setblocking(False)
            spawn = check_rad_food(foods=foods)
            player = PlayerSet(conn=new_socket, addr=addr,
                               x_pos=spawn.x,
                               y_pos=spawn.y,
                               radius=PLAYER_RADIUS,
                               colour=choice(PLAYER_COLOURS))
            spawn.reset()
            player.conn.send((' '.join([player.colour, str(player.radius)])).encode())
            all_players.append(player)
            print(f'new players')
    except:
        pass


    players_len = len(all_players)
    food_len = len(foods)
    #reset foods and moobs
    if tick % 200 == 0:

        #bots
        if players_len + 3 < BOTS_QUANTITY:
            for i in range(3):
                spawn = check_rad_food(foods=foods)
                bot = PlayerSet(x_pos=spawn.x,
                                y_pos=spawn.y,
                                radius=randint(25, 100),
                                colour=choice(PLAYER_COLOURS))
                vector = (randint(0, WIDTH_WINDOW) - WIDTH_WINDOW // 2,
                          randint(0, HEIGHT_WINDOW) - HEIGHT_WINDOW // 2)
                bot.update_move_vector(vector)
                all_players.append(bot)
                spawn.reset()

        #foods
        for food in foods:
            if food.radius == 0:
                food.reset()



    # receive new command from the players
    for player in all_players:
        if player.conn is not None:
            try:
                #players
                data = player.conn.recv(1024)
                data = data.decode()
                vector = get_correct_type(data)
                player.update_move_vector(vector)
            except:
                pass
        else:
            #bots
            if tick % 250 == 0:
                vector = (randint(0, WIDTH_WINDOW) - WIDTH_WINDOW // 2,
                          randint(0, HEIGHT_WINDOW) - HEIGHT_WINDOW // 2)
                player.update_move_vector(vector)
        player.upgrade_player()


    # determine what can see every player
    visible_balls = [ [] for ball in range(players_len)]
    try:
        for i in range(players_len):

            # compare with food
            for ind in range(len(foods)):
                x_dist = foods[ind].x - all_players[i].x_pos
                y_dist = foods[ind].y - all_players[i].y_pos

                if all_players[i].conn is not None:
                    visible_balls = check_visibility(all_players, visible_balls, x_dist, y_dist, i, ind, foods = foods)
                check_eating(all_players, x_dist, y_dist, i, ind, foods = foods)

            #compare with another bots/players
            for j in range(i + 1, players_len):
                x_dist = all_players[j].x_pos - all_players[i].x_pos
                y_dist = all_players[j].y_pos - all_players[i].y_pos

                check_eating(all_players, x_dist, y_dist, i, j)
                if all_players[i].conn is not None:
                    visible_balls = check_visibility(all_players, visible_balls, x_dist, y_dist, i, j)


                check_eating(all_players, x_dist, y_dist, j, i)
                if all_players[j].conn is not None:
                    visible_balls = check_visibility(all_players, visible_balls, -x_dist, -y_dist, j, i)
    except Exception as ex:
        print(ex)



    # # make response
    responses = []
    for i in range(players_len):
            if all_players[i].conn is not None:
                radius = str(round(all_players[i].radius/all_players[i].scale))
                x_pos = str(round(all_players[i].x_pos/all_players[i].scale))
                y_pos = str(round(all_players[i].y_pos/all_players[i].scale))
                scale = str(all_players[i].scale)
                response = ','.join([radius, x_pos, y_pos, scale])
                message = '<' + response + ',' + (','.join(visible_balls[i])) + '>'
                responses.append(message)
            else:
                responses.append('<>')



    # send new condition of the field if problem was appeared -> it means that player ended the game +
    for player in range(players_len):
        try:
            if all_players[player].conn is not None:
                all_players[player].conn.send(responses[player].encode())
                all_players[player].errors = 0
        except Exception as ex:
            all_players[player].errors += 1


    # disconnect players
    for player in all_players:
        if player.radius == 0:
            player.dead += 1 if player.conn is not None else 300
        if player.errors == 300 or (player.radius == 0 and player.dead > 299):
            if player.conn is not None:
                player.conn.close()
            all_players.remove(player)


    # draw server field
    if not server_running:
        screen.fill('gray20')
        for food in foods:
            x = round(food.x * WIDTH_SERVER_WIND / WIDTH_WINDOW)
            y = round(food.y * HEIGHT_SERVER_WIND / HEIGHT_WINDOW)
            r = round(food.radius * HEIGHT_SERVER_WIND / HEIGHT_WINDOW)
            colour = food.colour
            pygame.draw.circle(screen, colour, (x, y), r)

        for player in all_players:
            colour = player.colour
            window_x = round(player.x_pos * WIDTH_SERVER_WIND / WIDTH_WINDOW)
            window_y = round(player.y_pos * HEIGHT_SERVER_WIND / HEIGHT_WINDOW)
            radius = round(player.radius * HEIGHT_SERVER_WIND / HEIGHT_WINDOW)
            pygame.draw.circle(screen, colour, (window_x, window_y), radius)

        pygame.display.update()


    if tick > 1000:
        tick = 0

pygame.quit()
