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

    def get_rect(self):
        return (self.x, self.y, self.WIDTH, self.HEIGHT)

    def update_position(self, delta):
        self.x += self.dx * delta
        self.y += self.dy * delta
