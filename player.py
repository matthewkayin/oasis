import globals
import spells


class Player():
    def __init__(self):
        self.SPEED = 4
        self.WIDTH = 25
        self.HEIGHT = 50

        self.x = 0
        self.y = 0
        self.health = 3
        self.dx = 0
        self.dy = 0
        self.vx = 0
        self.vy = 0

        self.pending_spell = None
        self.charge_timer = 0
        self.active_spells = []

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
        if self.pending_spell is not None:
            if self.vx != 0 or self.vy != 0:
                self.pending_spell = None
                self.charge_timer = 0
            else:
                self.charge_timer -= delta
                if self.charge_timer <= 0:
                    self.active_spells.append(self.pending_spell)
                    self.charge_timer = 0
                    self.pending_spell = None

        self.x += self.vx * delta
        self.y += self.vy * delta

        remove_list = []
        for i in range(0, len(self.active_spells)):
            self.active_spells[i].update_position(delta)
            if self.active_spells[i].ended:
                remove_list.append(i)
        for index in remove_list:
            del self.active_spells[index]

    def get_charge_percent(self):
        if self.pending_spell is None:
            return 0
        else:
            return 1 - (self.charge_timer / self.pending_spell.CHARGE_TIME)

    def get_charge_bar_rect(self):
        return (self.x - 5, self.y - 10, 30 * self.get_charge_percent(), 5)

    def cast_fire(self, position):
        self.pending_spell = spells.Fire(self.get_center(), position)
        self.charge_timer = self.pending_spell.CHARGE_TIME
        self.set_dx(0)
        self.set_dy(0)
