import globals
import room


class Level():
    def __init__(self):
        self.PLAYER_SPEED = 3
        self.PLAYER_WIDTH = 20
        self.PLAYER_HEIGHT = 40

        self.CAMERA_RIGHT_THRESHOLD = int(1280 * 0.6)
        self.CAMERA_LEFT_THRESHOLD = int(1280 * 0.4)
        self.CAMERA_TOP_THRESHOLD = int(720 * 0.4)
        self.CAMERA_BOT_THRESHOLD = int(720 * 0.6)

        self.begin()

    def begin(self):
        self.gamestate = 1
        self.input_queue = []
        self.input_states = {}
        self.mouse_x = 0
        self.mouse_y = 0

        self.player_x = 70
        self.player_y = 70
        self.player_dx = 0
        self.player_dy = 0

        self.camera_x = 0
        self.camera_y = 0

        self.room = room.Room("A")
        self.room.create_exit("TOP")
        self.room.create_exit("RIGHT")
        self.room.create_exit("BOT")
        self.room.create_exit("LEFT")

    def get_player_rect(self):
        return (self.player_x, self.player_y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

    def offset_with_camera(self, rect):
        return (rect[0] - self.camera_x, rect[1] - self.camera_y, rect[2], rect[3])

    def input_output(self, input_queue, input_states, mouse_x, mouse_y):
        self.input_queue = input_queue
        self.input_states = input_states
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        return self.gamestate

    def check_collisions(self, delta):
        player_rect = self.get_player_rect()
        for collider_rect in self.room.colliders:
            if globals.rects_collide(player_rect, collider_rect):
                # We have a collision, so let's first revert player to pre-collision coords
                x_step = self.player_dx * delta
                y_step = self.player_dy * delta
                self.player_x -= x_step
                self.player_y -= y_step

                # Now check if collision is caused by x dir or y dir movement
                self.player_x += x_step
                player_rect = self.get_player_rect()
                x_causes_collision = globals.rects_collide(player_rect, collider_rect)
                self.player_x -= x_step

                self.player_y += y_step
                player_rect = self.get_player_rect()
                y_causes_collision = globals.rects_collide(player_rect, collider_rect)
                self.player_y -= y_step

                # If x movement doesn't cause collision, go ahead and keep doing x movement
                if not x_causes_collision:
                    self.player_x += x_step
                # Same thing with y direction
                if not y_causes_collision:
                    self.player_y += y_step

                player_rect = self.get_player_rect()

    def update_camera(self):
        if self.player_x - self.camera_x > self.CAMERA_RIGHT_THRESHOLD:
            self.camera_x += (self.player_x - self.camera_x) - self.CAMERA_RIGHT_THRESHOLD
        elif self.player_x - self.camera_x < self.CAMERA_LEFT_THRESHOLD:
            self.camera_x -= self.CAMERA_LEFT_THRESHOLD - (self.player_x - self.camera_x)

        if self.player_y - self.camera_y > self.CAMERA_BOT_THRESHOLD:
            self.camera_y += (self.player_y - self.camera_y) - self.CAMERA_BOT_THRESHOLD
        elif self.player_y - self.camera_y < self.CAMERA_TOP_THRESHOLD:
            self.camera_y -= self.CAMERA_TOP_THRESHOLD - (self.player_y - self.camera_y)

        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > self.room.WIDTH - 1280:
            self.camera_x = self.room.WIDTH - 1280

        if self.camera_y < 0:
            self.camera_y = 0
        elif self.camera_y > self.room.HEIGHT - 720:
            self.camera_y = self.room.HEIGHT - 720

    def update(self, delta):
        if delta == 0 or len(self.input_states) == 0:
            return

        while len(self.input_queue) != 0:
            event = self.input_queue.pop()
            if event == ("PLAYER UP", True):
                self.player_dy = -self.PLAYER_SPEED
            elif event == ("PLAYER RIGHT", True):
                self.player_dx = self.PLAYER_SPEED
            elif event == ("PLAYER DOWN", True):
                self.player_dy = self.PLAYER_SPEED
            elif event == ("PLAYER LEFT", True):
                self.player_dx = -self.PLAYER_SPEED
            elif event == ("PLAYER UP", False):
                if self.input_states["PLAYER DOWN"]:
                    self.player_dy = self.PLAYER_SPEED
                else:
                    self.player_dy = 0
            elif event == ("PLAYER RIGHT", False):
                if self.input_states["PLAYER LEFT"]:
                    self.player_dx = -self.PLAYER_SPEED
                else:
                    self.player_dx = 0
            elif event == ("PLAYER DOWN", False):
                if self.input_states["PLAYER UP"]:
                    self.player_dy = -self.PLAYER_SPEED
                else:
                    self.player_dy = 0
            elif event == ("PLAYER LEFT", False):
                if self.input_states["PLAYER RIGHT"]:
                    self.player_dx = self.PLAYER_SPEED
                else:
                    self.player_dx = 0

        self.player_x += self.player_dx * delta
        self.player_y += self.player_dy * delta

        self.check_collisions(delta)
        self.update_camera()

    def render(self, window):
        for collider_rect in self.room.colliders:
            window.fill_rect(window.RED, self.offset_with_camera(collider_rect))
        window.fill_rect(window.BLUE, self.offset_with_camera(self.get_player_rect()))
