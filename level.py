import globals
import map
import player


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

        self.player = player.Player()
        self.player.x = 70
        self.player.y = 70

        self.camera_x = 0
        self.camera_y = 0

        self.map = map.Map()

    def offset_with_camera(self, rect):
        return (rect[0] - self.camera_x, rect[1] - self.camera_y, rect[2], rect[3])

    def input_output(self, input_queue, input_states, mouse_x, mouse_y):
        self.input_queue = input_queue
        self.input_states = input_states
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        return self.gamestate

    def check_collisions(self, delta):
        player_rect = self.player.get_rect()
        for collider_rect in self.map.rooms[self.map.current_room].colliders:
            if globals.rects_collide(player_rect, collider_rect):
                # We have a collision, so let's first revert player to pre-collision coords
                x_step = self.player.dx * delta
                y_step = self.player.dy * delta
                self.player.x -= x_step
                self.player.y -= y_step

                # Now check if collision is caused by x dir or y dir movement
                self.player.x += x_step
                player_rect = self.player.get_rect()
                x_causes_collision = globals.rects_collide(player_rect, collider_rect)
                self.player.x -= x_step

                self.player.y += y_step
                player_rect = self.player.get_rect()
                y_causes_collision = globals.rects_collide(player_rect, collider_rect)
                self.player.y -= y_step

                # If x movement doesn't cause collision, go ahead and keep doing x movement
                if not x_causes_collision:
                    self.player.x += x_step
                # Same thing with y direction
                if not y_causes_collision:
                    self.player.y += y_step

                player_rect = self.player.get_rect()

    def check_exits(self):
        player_rect = self.player.get_rect()
        for i in range(0, len(self.map.rooms[self.map.current_room].exit)):
            exit_rect = self.map.rooms[self.map.current_room].exit[i]
            if globals.rects_collide(player_rect, exit_rect) and not globals.rects_collide(player_rect, self.map.rooms[self.map.current_room].get_rect()):
                new_player_coords = self.map.take_exit(i, (self.player.x, self.player.y))
                self.player.x = new_player_coords[0]
                self.player.y = new_player_coords[1]

                return

    def update_camera(self):
        if self.player.x - self.camera_x > self.CAMERA_RIGHT_THRESHOLD:
            self.camera_x += (self.player.x - self.camera_x) - self.CAMERA_RIGHT_THRESHOLD
        elif self.player.x - self.camera_x < self.CAMERA_LEFT_THRESHOLD:
            self.camera_x -= self.CAMERA_LEFT_THRESHOLD - (self.player.x - self.camera_x)

        if self.player.y - self.camera_y > self.CAMERA_BOT_THRESHOLD:
            self.camera_y += (self.player.y - self.camera_y) - self.CAMERA_BOT_THRESHOLD
        elif self.player.y - self.camera_y < self.CAMERA_TOP_THRESHOLD:
            self.camera_y -= self.CAMERA_TOP_THRESHOLD - (self.player.y - self.camera_y)

        if self.camera_x < 0:
            self.camera_x = 0
        elif self.camera_x > self.map.rooms[self.map.current_room].WIDTH - 1280:
            self.camera_x = self.map.rooms[self.map.current_room].WIDTH - 1280

        if self.camera_y < 0:
            self.camera_y = 0
        elif self.camera_y > self.map.rooms[self.map.current_room].HEIGHT - 720:
            self.camera_y = self.map.rooms[self.map.current_room].HEIGHT - 720

    def handle_input(self):
        while len(self.input_queue) != 0:
            event = self.input_queue.pop()
            if event == ("PLAYER UP", True):
                self.player.dy = -self.PLAYER_SPEED
            elif event == ("PLAYER RIGHT", True):
                self.player.dx = self.PLAYER_SPEED
            elif event == ("PLAYER DOWN", True):
                self.player.dy = self.PLAYER_SPEED
            elif event == ("PLAYER LEFT", True):
                self.player.dx = -self.PLAYER_SPEED
            elif event == ("PLAYER UP", False):
                if self.input_states["PLAYER DOWN"]:
                    self.player.dy = self.PLAYER_SPEED
                else:
                    self.player.dy = 0
            elif event == ("PLAYER RIGHT", False):
                if self.input_states["PLAYER LEFT"]:
                    self.player.dx = -self.PLAYER_SPEED
                else:
                    self.player.dx = 0
            elif event == ("PLAYER DOWN", False):
                if self.input_states["PLAYER UP"]:
                    self.player.dy = -self.PLAYER_SPEED
                else:
                    self.player.dy = 0
            elif event == ("PLAYER LEFT", False):
                if self.input_states["PLAYER RIGHT"]:
                    self.player.dx = self.PLAYER_SPEED
                else:
                    self.player.dx = 0

    def update_enemies(self, delta):
        for enemy in self.map.rooms[self.map.current_room].enemies:
            enemy.update_position(delta, self.player.get_center())
            self.player.health -= enemy.get_damage()

    def update(self, delta):
        if delta == 0 or len(self.input_states) == 0:
            return

        self.handle_input()
        self.player.update_position(delta)
        self.check_collisions(delta)
        self.check_exits()
        self.update_enemies(delta)
        self.update_camera()

    def render(self, window):
        for collider_rect in self.map.rooms[self.map.current_room].colliders:
            window.fill_rect(window.GREEN, self.offset_with_camera(collider_rect))
        for enemy in self.map.rooms[self.map.current_room].enemies:
            if enemy.attacking:
                window.fill_rect(window.RED, self.offset_with_camera(enemy.get_rect()))
            else:
                window.fill_rect(window.WHITE, self.offset_with_camera(enemy.get_rect()))
        window.fill_rect(window.BLUE, self.offset_with_camera(self.player.get_rect()))
        for i in range(0, self.player.health):
            window.fill_rect(window.YELLOW, (10 + (i * 50), 10, 40, 40))
