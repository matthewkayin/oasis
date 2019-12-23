import globals
import spells
import items


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
        self.pending_remove_index = 0
        self.charge_timer = 0
        self.active_spells = []

        self.ui_state = 0
        self.ui_substate = 0

        self.inventory = []
        self.add_item("spellbook-fire", 3)

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
                    self.inventory[self.pending_remove_index].quantity -= 1
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

        remove_list = []
        for i in range(0, len(self.inventory)):
            if self.inventory[i].quantity == 0:
                remove_list.append(i)
        for index in remove_list:
            del self.inventory[index]

    def get_castable_spells(self):
        castables = []
        for item in self.inventory:
            if item.type == "spellbook":
                castables.append((item.shortname[item.shortname.index("-") + 1:], item.quantity))

        return castables

    def get_inventory_position(self, item_shortname):
        for i in range(0, len(self.inventory)):
            if self.inventory[i].shortname == item_shortname:
                return i

        return -1

    def add_item(self, shortname, quantity=1):
        index = self.get_inventory_position(shortname)
        if index == -1:
            self.inventory.append(items.Item(shortname, quantity))
        else:
            self.inventory[index].quantity += quantity

    def get_charge_percent(self):
        if self.pending_spell is None:
            return 0
        else:
            return 1 - (self.charge_timer / self.pending_spell.CHARGE_TIME)

    def get_charge_bar_rect(self):
        return (self.x - 5, self.y - 10, 30 * self.get_charge_percent(), 5)

    def cast_spell(self, shortname, position):
        spell = None
        if shortname == "fire":
            spell = spells.Fire(self.get_center(), position)
        else:
            print("Invalid spell shortname in cast_spell!")
            return
        if globals.point_distance(position, self.get_center()) > spell.CAST_RADIUS:
            return

        self.ui_state = 0
        self.ui_substate = 0
        self.pending_remove_index = self.get_inventory_position("spellbook-" + shortname)
        self.pending_spell = spell
        self.charge_timer = self.pending_spell.CHARGE_TIME
        self.set_dx(0)
        self.set_dy(0)
