import globals


class Fire():
    def __init__(self, source_pos, target_pos):
        # The target position will be the center of the effect
        self.CAST_RADIUS = 400
        self.PROJECTILE_WIDTH = 10
        self.PROJECTILE_HEIGHT = 10
        self.PROJECTILE_SPEED = 6
        self.WIDTH = 40
        self.HEIGHT = 40
        self.DURATION = 60
        self.CHARGE_TIME = 15

        self.x, self.y = source_pos
        distance_vector = (target_pos[0] - self.x, target_pos[1] - self.y)
        self.vx, self.vy = globals.scale_vector(distance_vector, self.PROJECTILE_SPEED)
        self.tx, self.ty = target_pos

        if globals.point_distance(source_pos, target_pos) > self.CAST_RADIUS:
            self.ended = True
        else:
            self.ended = False
        self.damage = 1
        self.state = 0
        self.timer = self.DURATION

    def get_rect(self):
        if self.state == 0:
            return (self.x, self.y, self.PROJECTILE_WIDTH, self.PROJECTILE_HEIGHT)
        else:
            return (self.x, self.y, self.WIDTH, self.HEIGHT)

    def get_damage(self):
        if self.state == 0:
            return 0
        elif self.state == 1:
            return self.damage

    def update_position(self, delta):
        if self.state == 0:
            if globals.point_distance((self.x, self.y), (self.tx, self.ty)) < 5:
                self.state = 1
                self.x = self.tx - (self.WIDTH / 2)
                self.y = self.ty - (self.HEIGHT / 2)
                self.vx = 0
                self.vy = 0
            else:
                self.x += self.vx * delta
                self.y += self.vy * delta
        elif self.state == 1:
            self.timer -= delta
            if self.timer <= 0:
                self.ended = True
