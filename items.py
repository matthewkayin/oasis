class Item():
    database = {}
    database["spellbook-fire"] = ["Fire Spellbook", "spellbook", "Cast flames onto the ground for 1 second."]

    def __init__(self, shortname, quantity=1):
        database_entry = Item.database[shortname]
        self.shortname = shortname
        self.name = database_entry[0]
        self.type = database_entry[1]
        self.desc = database_entry[2]
        self.quantity = quantity
