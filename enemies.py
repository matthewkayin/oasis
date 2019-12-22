import globals


class Enemy():
    def __init__(self):
        self.SPEED = 2.5
        self.WIDTH = 25
        self.HEIGHT = 40
        self.LINE_OF_SIGHT = 250
        self.ATTACK_RANGE = 25

        self.x = 0
        self.y = 0
        self.health = 1
        self.dx = 0
        self.dy = 0
        self.vx = 0
        self.vy = 0

        self.attacking = False
        self.attack_timer = 0
        self.ATTACK_WINDUP = 20
        self.POWER = 1
        self.damage = 0
        self.hurtbox = None
        self.health = 1

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

    def update_position(self, delta, player_rect):
        if self.damage > 0:
            self.damage = 0
            self.hurtbox = None

        player_pos = globals.get_center(player_rect)
        player_distance = globals.point_distance(player_pos, self.get_center())

        if self.attacking:
            self.attack_timer -= delta
            if self.attack_timer <= 0:
                self.damage = self.POWER
                self.attacking = False
        elif player_distance <= self.ATTACK_RANGE:
            self.set_dx(0)
            self.set_dy(0)
            self.attacking = True
            self.attack_timer = self.ATTACK_WINDUP
            self.hurtbox = player_rect
        elif player_distance <= self.LINE_OF_SIGHT:
            if abs(player_pos[0] - self.get_center()[0]) > (self.ATTACK_RANGE / 2):
                if player_pos[0] > self.get_center()[0]:
                    self.set_dx(1)
                else:
                    self.set_dx(-1)
            else:
                self.set_dx(0)
            if abs(player_pos[1] - self.get_center()[1]) > (self.ATTACK_RANGE / 2):
                if player_pos[1] > self.get_center()[1]:
                    self.set_dy(1)
                else:
                    self.set_dy(-1)
            else:
                self.set_dy(0)

        self.x += self.vx * delta
        self.y += self.vy * delta
