import enemies


class Map():
    def __init__(self):
        self.current_room = 0
        self.rooms = []

        self.rooms.append(Room("A", 0, 0))
        self.rooms[0].create_exit("TOP")
        self.rooms.append(Room("B", 0, -720))
        self.rooms[1].create_exit("BOT")

    def get_current_room(self):
        return self.rooms[self.current_room]


class Room():
    def __init__(self, tag, x, y):
        self.colliders = []
        self.enemies = []
        self.floor_tiles = []
        self.base_x = x
        self.base_y = y
        self.WIDTH = 0
        self.HEIGHT = 0
        self.WALL_SIZE = 40
        if tag == "A":
            self.generate_a()
        elif tag == "B":
            self.generate_b()
        elif tag == "C":
            self.generate_c()

        # Generate floor tiles now that we know the width
        remaining_height = self.HEIGHT
        tile_y = self.base_y
        while remaining_height > 0:
            tile_height = min(remaining_height, 80)
            remaining_height -= tile_height
            remaining_width = self.WIDTH
            tile_x = self.base_x
            while remaining_width > 0:
                tile_width = min(remaining_width, 80)
                remaining_width -= tile_width
                self.floor_tiles.append((tile_x, tile_y, tile_width, tile_height))
                tile_x += tile_width
            tile_y += tile_height

    def get_rect(self):
        return (0, 0, self.WIDTH, self.HEIGHT)

    def add_collider(self, rect):
        self.colliders.append((rect[0] + self.base_x, rect[1] + self.base_y, rect[2], rect[3]))

    def insert_collider(self, index, rect):
        self.colliders.insert(index, (rect[0] + self.base_x, rect[1] + self.base_y, rect[2], rect[3]))

    def generate_walls(self):
        self.add_collider((0, 0, self.WIDTH, self.WALL_SIZE))
        self.add_collider((0, self.HEIGHT - self.WALL_SIZE, self.WIDTH, self.WALL_SIZE))
        self.add_collider((0, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))
        self.add_collider((self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, self.HEIGHT - (self.WALL_SIZE * 2)))

    def create_exit(self, direction):
        if direction == "TOP":
            new_wall_left = (0, 0, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), 0, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[0]
            self.insert_collider(0, new_wall_left)
            self.add_collider(new_wall_right)
        elif direction == "BOT":
            new_wall_left = (0, self.HEIGHT - self.WALL_SIZE, (self.WIDTH - (self.WALL_SIZE * 2)) / 2, self.WALL_SIZE)
            new_wall_right = (new_wall_left[2] + (self.WALL_SIZE * 2), self.HEIGHT - self.WALL_SIZE, new_wall_left[2], self.WALL_SIZE)

            del self.colliders[1]
            self.insert_collider(1, new_wall_left)
            self.add_collider(new_wall_right)
        elif direction == "LEFT":
            new_wall_top = (0, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (0, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[2]
            self.insert_collider(2, new_wall_top)
            self.add_collider(new_wall_bot)
        elif direction == "RIGHT":
            new_wall_top = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE, self.WALL_SIZE, (self.HEIGHT - (self.WALL_SIZE * 4)) / 2)
            new_wall_bot = (self.WIDTH - self.WALL_SIZE, self.WALL_SIZE + new_wall_top[3] + (self.WALL_SIZE * 2), self.WALL_SIZE, new_wall_top[3])

            del self.colliders[3]
            self.insert_collider(3, new_wall_top)
            self.add_collider(new_wall_bot)

    def generate_a(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.generate_walls()
        self.enemies.append(enemies.Enemy())
        self.enemies[0].x = 1000 + self.base_x
        self.enemies[0].y = 200 + self.base_y

    def generate_b(self):
        self.WIDTH = 1280
        self.HEIGHT = 720
        self.generate_walls()
        self.add_collider((540, 300, 40, 40))
        self.add_collider((540 + 80, 300, 40, 40))

    def generate_c(self):
        self.WIDTH = 1280 * 2
        self.HEIGHT = 720 * 2
        self.generate_walls()

        self.add_collider((540, 300, 40, 40))
        self.add_collider((540 + 80, 300, 40, 40))

        self.add_collider((1280 + 540, 300, 40, 40))
        self.add_collider((1280 + 540 + 80, 300, 40, 40))

        self.add_collider((1280 + 540, 720 + 300, 40, 40))
        self.add_collider((1280 + 540 + 80, 720 + 300, 40, 40))

        self.add_collider((540, 720 + 300, 40, 40))
        self.add_collider((540 + 80, 720 + 300, 40, 40))
