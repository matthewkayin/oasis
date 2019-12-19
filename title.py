import globals


class Title():
    def __init__(self):
        self.menu_options = ["Play", "Controls", "Exit"]
        self.menu_rects = []
        for i in range(0, len(self.menu_options)):
            self.menu_rects.append((540, 300 + (90 * i), 200, 60))
        self.begin()

    def begin(self):
        self.gamestate = 0
        self.input_queue = []
        self.input_states = {}
        self.mouse_x = 0
        self.mouse_y = 0

        self.menu_index = -1

    def input_output(self, input_queue, input_states, mouse_x, mouse_y):
        self.input_queue = input_queue
        self.input_states = input_states
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y

        # We return gamestate to control state-to-state flow
        return self.gamestate

    def update(self, delta):
        if delta == 0:
            return

        self.menu_index = -1
        for i in range(0, len(self.menu_options)):
            if globals.point_in_rect(self.mouse_x, self.mouse_y, self.menu_rects[i]):
                self.menu_index = i

        while len(self.input_queue) != 0:
            event = self.input_queue.pop()
            if event == ("LEFT CLICK", True):
                if self.menu_index == 0:
                    self.gamestate = 1
                elif self.menu_index == 2:
                    self.gamestate = -1  # This will tell main to stop running the game

    def render(self, window):
        window.render_text("OASIS", ("CENTERED", 70), 96)
        for i in range(0, len(self.menu_options)):
            # option = self.menu_options[i]
            if i == self.menu_index:
                window.fill_rect(window.WHITE, self.menu_rects[i])
                window.render_text(self.menu_options[i], (560, 300 + (90 * i) + 10), 32, window.BLACK)
            else:
                window.draw_rect(window.WHITE, self.menu_rects[i])
                window.render_text(self.menu_options[i], (560, 300 + (90 * i) + 10), 32, window.WHITE)
