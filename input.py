import pygame


class Input():
    def __init__(self, input_names):
        self.user_exits = False

        self.names = input_names
        self.map = {}
        self.queue = []
        self.states = {}
        for name in self.names:
            self.states[name] = False
        self.mouse_x = 0
        self.mouse_y = 0

    def map_key(self, pygame_key, input_name):
        self.map[pygame_key] = input_name

    def handle_input(self, pygame_key, new_state):
        if pygame_key not in list(self.map.keys()):
            return
        input_name = self.map[pygame_key]

        # If this action doesn't change the current state, don't do anything
        # This prevents overloading the queue with repeat button events for a held button
        if self.states[input_name] == new_state:
            return

        self.states[input_name] = new_state
        self.queue.insert(0, (input_name, new_state))

    def plug_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.user_exits = True
            elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                self.handle_input(event.key, event.type == pygame.KEYDOWN)
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
                self.handle_input("M" + str(event.button), event.type == pygame.MOUSEBUTTONDOWN)
            elif event.type == pygame.MOUSEMOTION:
                pos = pygame.mouse.get_pos()
                self.mouse_x = pos[0]
                self.mouse_y = pos[1]

    def clear_input_queue(self):
        self.input_queue = []
