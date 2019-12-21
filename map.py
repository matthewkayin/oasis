import enemies


class Map():
    def __init__(self):
        self.current_room = 0
        self.rooms = []

        self.rooms.append(Room("A"))
        self.rooms[0].create_exit("TOP", (1, 0))
        self.rooms.append(Room("B"))
        self.rooms[1].create_exit("BOT", (0, 0))

    def get_current_room(self):
        return self.rooms[self.current_room]

    def take_exit(self, index, player_coords):
        player_relative_x = player_coords[0] - self.rooms[self.current_room].exit[index][0]
        player_relative_y = player_coords[1] - self.rooms[self.current_room].exit[index][1]
        exit_coords = self.rooms[self.current_room].exit_coords[index]
        exit_orientation = self.rooms[self.current_room].exit_orientations[index]

        self.current_room = exit_coords[0]
        entrance_rect = list(self.rooms[self.current_room].exit[exit_coords[1]])
        if exit_orientation == "TOP":
            entrance_rect[1] -= self.rooms[self.current_room].WALL_SIZE
        elif exit_orientation == "RIGHT":
            entrance_rect[0] += self.rooms[self.current_room].WALL_SIZE
        if exit_orientation == "BOT":
            entrance_rect[1] += self.rooms[self.current_room].WALL_SIZE
        if exit_orientation == "LEFT":
            entrance_rect[0] -= self.rooms[self.current_room].WALL_SIZE

        new_player_x = entrance_rect[0] + player_relative_x
        new_player_y = entrance_rect[1] + player_relative_y
        return (new_player_x, new_player_y)


class Room():
    def __init__(self, tag):
        self.colliders = []
        self.exit = []
        self.exit_coords = []
        self.exit_orientations = []
        self.enemies = []
        self.WIDTH = 0
        self.HEIGHT = 0
        self.WALL_SIZE = 40
        if tag == "A":
            self.generate_a()
        elif tag == "B":
            self.generate_b()
        elif tag == "C":
            self.generate_c()

    def get_rect(self):
        return (0, 0, self.WIDTH, self.HEIGHT)

    def generate_walls(self):
        self.colliders.append((0, 0, self.WIDTH, self.WALL_SIZE))
        self.colliders.append((0, self.HEIGHT - self.WALL_SIZE, self.WIDTH, self.WALL_SIZE))
        self.colliders.append((0, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))
        self.colliders.append((self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))

    def create_exit(self, direction, coords):
        if direction == "TOP":
            new_wall_left = (0, 0, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), 0, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[0]
            self.colliders.insert(0, new_wall_left)
            self.colliders.append(new_wall_right)

            self.exit.append((new_wall_left[2], -self.WALL_SIZE, self.WALL_SIZE * 2, self.WALL_SIZE))
        elif direction == "BOT":
            new_wall_left = (0, self.HEIGHT - self.WALL_SIZE, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), self.HEIGHT - self.WALL_SIZE, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[1]
            self.colliders.insert(1, new_wall_left)
            self.colliders.append(new_wall_right)

            self.exit.append((new_wall_left[2], self.HEIGHT + self.WALL_SIZE, self.WALL_SIZE * 2, self.WALL_SIZE))
        elif direction == "LEFT":
            new_wall_top = (0, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (0, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[2]
            self.colliders.insert(2, new_wall_top)
            self.colliders.append(new_wall_bot)

            self.exit.append((0, new_wall_top[3], self.WALL_SIZE, self.WALL_SIZE * 2))
        elif direction == "RIGHT":
            new_wall_top = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[3]
            self.colliders.insert(3, new_wall_top)
            self.colliders.append(new_wall_bot)

            self.exit.append((self.WIDTH + self.WALL_SIZE, new_wall_top[3], self.WALL_SIZE, self.WALL_SIZE * 2))

        self.exit_coords.append(coords)
        self.exit_orientations.append(direction)

    def generate_a(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.generate_walls()
        self.enemies.append(enemies.Enemy())
        self.enemies[0].x = 1000
        self.enemies[0].y = 200

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
