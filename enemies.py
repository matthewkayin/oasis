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

        self.attacking = False
        self.attack_timer = 0
        self.ATTACK_WINDUP = 20
        self.POWER = 1
        self.damage = 0
        self.hurtbox = None

    def get_rect(self):
        return (self.x, self.y, self.WIDTH, self.HEIGHT)

    def get_center(self):
        return (self.x + (self.WIDTH / 2), self.y + (self.HEIGHT / 2))

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
            self.dx = 0
            self.dy = 0
            self.attacking = True
            self.attack_timer = self.ATTACK_WINDUP
            self.hurtbox = player_rect
        elif player_distance <= self.LINE_OF_SIGHT:
            if abs(player_pos[0] - self.get_center()[0]) > (self.ATTACK_RANGE / 2):
                if player_pos[0] > self.get_center()[0]:
                    self.dx = self.SPEED
                else:
                    self.dx = -self.SPEED
            else:
                self.dx = 0
            if abs(player_pos[1] - self.get_center()[1]) > (self.ATTACK_RANGE / 2):
                if player_pos[1] > self.get_center()[1]:
                    self.dy = self.SPEED
                else:
                    self.dy = -self.SPEED
            else:
                self.dy = 0

        self.x += self.dx * delta
        self.y += self.dy * delta
