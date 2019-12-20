class Room():
    def __init__(self, tag):
        self.colliders = []
        self.exits = []
        self.WIDTH = 0
        self.HEIGHT = 0
        self.WALL_SIZE = 40
        if tag == "A":
            self.generate_a()
        elif tag == "B":
            self.generate_b()
        elif tag == "C":
            self.generate_c()

    def generate_walls(self):
        self.colliders.append((0, 0, self.WIDTH, self.WALL_SIZE))
        self.colliders.append((0, self.HEIGHT - self.WALL_SIZE, self.WIDTH, self.WALL_SIZE))
        self.colliders.append((0, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))
        self.colliders.append((self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))

    def create_exit(self, direction):
        if direction == "TOP":
            new_wall_left = (0, 0, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), 0, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[0]
            self.colliders.insert(0, new_wall_left)
            self.colliders.append(new_wall_right)

            self.exits.append((new_wall_left[2], -self.WALL_SIZE, self.WALL_SIZE * 2, self.WALL_SIZE))
        if direction == "BOT":
            new_wall_left = (0, self.HEIGHT - self.WALL_SIZE, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), self.HEIGHT - self.WALL_SIZE, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[1]
            self.colliders.insert(1, new_wall_left)
            self.colliders.append(new_wall_right)

            self.exits.append((new_wall_left[2], self.HEIGHT + self.WALL_SIZE, self.WALL_SIZE * 2, self.WALL_SIZE))
        if direction == "LEFT":
            new_wall_top = (0, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (0, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[2]
            self.colliders.insert(2, new_wall_top)
            self.colliders.append(new_wall_bot)

            self.exits.append((0, new_wall_top[3], self.WALL_SIZE, self.WALL_SIZE * 2))
        if direction == "RIGHT":
            new_wall_top = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[3]
            self.colliders.insert(3, new_wall_top)
            self.colliders.append(new_wall_bot)

            self.exits.append((0, new_wall_top[3], self.WALL_SIZE, self.WALL_SIZE * 2))

    def generate_a(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.generate_walls()

    def generate_b(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.generate_walls()
        self.colliders.append((540, 300, 40, 40))
        self.colliders.append((540 + 80, 300, 40, 40))

    def generate_c(self):
        self.WIDTH = 1280 * 2
        self.HEIGHT = 720 * 2
        self.generate_walls()

        self.colliders.append((540, 300, 40, 40))
        self.colliders.append((540 + 80, 300, 40, 40))

        self.colliders.append((1280 + 540, 300, 40, 40))
        self.colliders.append((1280 + 540 + 80, 300, 40, 40))

        self.colliders.append((1280 + 540, 720 + 300, 40, 40))
        self.colliders.append((1280 + 540 + 80, 720 + 300, 40, 40))

        self.colliders.append((540, 720 + 300, 40, 40))
        self.colliders.append((540 + 80, 720 + 300, 40, 40))
