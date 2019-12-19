import globals


class Level():
    def __init__(self):
        self.PLAYER_SPEED = 3
        self.PLAYER_WIDTH = 20
        self.PLAYER_HEIGHT = 40
        self.TILE_WIDTH = 64
        self.TILE_HEIGHT = 64

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

        self.map = []
        self.generate_map()

    def generate_map(self):
        self.map = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

    def get_tile_rect(self, x, y):
        return (x * self.TILE_WIDTH, y * self.TILE_HEIGHT, self.TILE_WIDTH, self.TILE_HEIGHT)

    def get_player_rect(self):
        return (self.player_x, self.player_y, self.PLAYER_WIDTH, self.PLAYER_HEIGHT)

    def input_output(self, input_queue, input_states, mouse_x, mouse_y):
        self.input_queue = input_queue
        self.input_states = input_states
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        return self.gamestate

    def check_collisions(self, delta):
        player_rect = self.get_player_rect()
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                if self.map[y][x] == 1:
                    if globals.rects_collide(player_rect, self.get_tile_rect(x, y)):
                        # We have a collision, so let's first revert player to pre-collision coords
                        x_step = self.player_dx * delta
                        y_step = self.player_dy * delta
                        self.player_x -= x_step
                        self.player_y -= y_step

                        # Now check if collision is caused by x dir or y dir movement
                        self.player_x += x_step
                        player_rect = self.get_player_rect()
                        x_causes_collision = globals.rects_collide(player_rect, self.get_tile_rect(x, y))
                        self.player_x -= x_step

                        self.player_y += y_step
                        player_rect = self.get_player_rect()
                        y_causes_collision = globals.rects_collide(player_rect, self.get_tile_rect(x, y))
                        self.player_y -= y_step

                        # If x movement doesn't cause collision, go ahead and keep doing x movement
                        if not x_causes_collision:
                            self.player_x += x_step
                        # Same thing with y direction
                        if not y_causes_collision:
                            self.player_y += y_step

                        player_rect = self.get_player_rect()

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
        """
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                if self.map[y][x] == 1:
                    if globals.rects_collide(self.get_player_rect(), self.get_tile_rect(x, y)):
                        self.player_x -= self.player_dx * delta
                        self.player_y -= self.player_dy * delta
        """

    def render(self, window):
        for y in range(0, len(self.map)):
            for x in range(0, len(self.map[0])):
                if self.map[y][x] == 1:
                    window.fill_rect(window.RED, self.get_tile_rect(x, y))
        window.fill_rect(window.BLUE, self.get_player_rect())
