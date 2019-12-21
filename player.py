import globals


class Player():
    def __init__(self):
        self.SPEED = 3
        self.WIDTH = 20
        self.HEIGHT = 40

        self.x = 0
        self.y = 0
        self.health = 3
        self.dx = 0
        self.dy = 0
        self.vx = 0
        self.vy = 0

    def get_rect(self):
        return (self.x, self.y, self.WIDTH, self.HEIGHT)

    def get_center(self):
        return (self.x + (self.WIDTH / 2), self.y + (self.HEIGHT / 2))

    def set_dx(self, value):
        self.dx = value
        self.update_velocity()

    def set_dy(self, value):
        self.dy = value
        self.update_velocity()

    def update_velocity(self):
        self.vx, self.vy = globals.scale_vector((self.dx, self.dy), self.SPEED)

    def update_position(self, delta):
        self.x += self.vx * delta
        self.y += self.vy * delta
