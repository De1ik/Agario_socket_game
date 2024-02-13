from server_config import WIDTH_WINDOW, HEIGHT_WINDOW
# # check if the second ball can eat the first
#
#
# def check_visibility(all_players, index_1, index_2, visible_balls, x_dist, y_dist):
#
#                 if (((x_dist ** 2 + y_dist ** 2) ** 0.5 <= all_players[index_2].radius) and
#                         (all_players[index_2].radius > 1.1 * all_players[index_1].radius)):
#                     # change radius the win player
#                     # ----------------------------
#
#                     # delete player who was ate
#                     all_players[index_1].radius = all_players[index_1].sp_x = all_players[index_1].sp_y = 0
#
# #def possible_to_eat(all_players, index_1, index_2, visible_balls, x_dist, y_dist)
#                 # check if the first ball is in visibility of the second
#                 if all_players[index_2].conn is not None:
#                     if ((abs(x_dist) <= all_players[index_2].w_vision + all_players[index_1].radius)
#                             and
#                             (abs(y_dist) <= all_players[index_2].h_vision + all_players[index_1].radius)):
#                         x = str(round(x_dist))
#                         y = str(round(y_dist))
#                         radius = str(round(all_players[index_1].radius))
#                         col = all_players[index_1].colour
#                         visible_balls[index_2].append(' '.join([x, y, radius, col]))
#
#                 return visible_balls



def check_visibility(all_players, visible_balls, x_dist, y_dist, i, j, foods=None):
    template = all_players if foods is None else foods

    if ((abs(x_dist) <= all_players[i].w_vision + (template[j].radius/all_players[i].scale))
            and
            (abs(y_dist) <= all_players[i].h_vision + (template[j].radius/all_players[i].scale))):
        x = str(round(x_dist/all_players[i].scale))
        y = str(round(y_dist/all_players[i].scale))
        radius = str(round(template[j].radius/all_players[i].scale))
        col = template[j].colour
        visible_balls[i].append(' '.join([x, y, radius, col]))
    return visible_balls
#
def check_eating(all_players, x_dist, y_dist, ind_1, ind_2, foods = None):
    template = all_players if foods is None else foods
    k = 1.1 if foods is None else 1

    if (((x_dist ** 2 + y_dist ** 2) ** 0.5 <= all_players[ind_1].radius) and
            (all_players[ind_1].radius > k * template[ind_2].radius)):
        # change radius the win player
        r = (all_players[ind_1].radius**2 + template[ind_2].radius**2)**0.5
        if (r < WIDTH_WINDOW * HEIGHT_WINDOW / 6):
            all_players[ind_1].radius = r
        #all_players[ind_1].update_st_speed()


        # delete player who was ate
        if foods is None:
            all_players[ind_2].radius = all_players[ind_2].static_speed = 0
        else:
            foods[ind_2].radius = 0