class Level():
    def __init__(self):
        self.PLAYER_SPEED = 3

        self.begin()

    def begin(self):
        self.gamestate = 1
        self.input_queue = []
        self.input_states = {}
        self.mouse_x = 0
        self.mouse_y = 0

        self.player_x = 0
        self.player_y = 0
        self.player_dx = 0
        self.player_dy = 0

    def input_output(self, input_queue, input_states, mouse_x, mouse_y):
        self.input_queue = input_queue
        self.input_states = input_states
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        return self.gamestate

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

    def render(self, window):
        window.fill_rect(window.BLUE, (self.player_x, self.player_y, 20, 40))
