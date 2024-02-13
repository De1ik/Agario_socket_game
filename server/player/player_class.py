from server_config import WIDTH_WINDOW, HEIGHT_WINDOW, PLAYER_DEFAULT_HEIGHT_WINDOW, PLAYER_DEFAULT_WIDTH_WINDOW, PLAYER_RADIUS
#PLAYER_DEFAULT_HEIGHT_WINDOW, PLAYER_DEFAULT_WIDTH_WINDOW = 700, 1000

class PlayerSet:
    def __init__(self, x_pos, y_pos, radius, colour, conn=None, addr=None, sp_x=0, sp_y=0):
        self.conn = conn
        self.addr = addr
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.radius = radius
        self.colour = colour
        self.h_window = 700
        self.w_window = 1000

        self.scale = 1
        self.h_vision = round(self.scale * self.h_window)
        self.w_vision = round(self.scale * self.w_window)

        self.errors = 0
        self.dead = 0

        self.static_speed = 30/(self.radius**0.5)
        self.sp_x = sp_x
        self.sp_y = sp_y

    def update_move_vector(self, vector):
        x, y = vector
        #set vector for moving
        if x == y == 0:
            self.sp_x = 0
            self.sp_y = 0
        else:
            len_vector = (x**2 + y**2)**0.5
            self.sp_x = x / len_vector * self.static_speed
            self.sp_y = y / len_vector * self.static_speed


    def update_pos(self):
        self.x_pos += self.sp_x
        self.x_pos = 3999 if self.x_pos > 3999 else 0 if self.x_pos < 0 else self.x_pos
        self.y_pos += self.sp_y
        self.y_pos = 3999 if self.y_pos > 3999 else 0 if self.y_pos < 0 else self.y_pos

    def update_st_speed(self):
        self.static_speed = 30 / (self.radius ** 0.5)

    def update_scale(self):
        if (self.radius > self.w_vision/4) or (self.radius > self.h_vision/4):
            if (self.w_vision < WIDTH_WINDOW) or (self.h_vision < HEIGHT_WINDOW):
                self.scale *=2 #self.radius // PLAYER_RADIUS
                self.w_vision = self.w_window * self.scale
                self.h_vision = self.h_window * self.scale
                return True

        elif self.scale !=1 and self.radius != 0 and (self.radius < self.w_vision/8) and (self.radius < self.h_vision/8):
            if (self.w_vision < WIDTH_WINDOW) and (self.h_vision < HEIGHT_WINDOW):
                self.scale //=2
                self.w_vision = self.w_window * self.scale
                self.h_vision = self.h_window * self.scale
                return True

    def change_radius(self):
        self.radius -=self.radius/18000

    def upgrade_player(self):
        try:
            self.update_pos()
            self.update_st_speed()
            self.change_radius()
            self.update_scale()
        except:
            pass
        #self.update_move_vector(vector)

