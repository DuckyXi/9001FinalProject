class Minion:
    def __init__(self, name, tier, attack, health, keywords, tribe, image_path, description, derivant=False):
        self.name = name
        self.tier = tier
        self.attack = attack
        self.health = health
        self.keywords = keywords
        self.tribe = tribe
        self.image_path = image_path
        self.description = description
        self.derivant = derivant
        self.buffs = {}

    def isAlive(self):
        return self.health > 0

    def attack_enemy(self):
        pass

class Spell:
    def __init__(self, name, tier, cost, image_path, description, have_target):
        self.name = name
        self.tier = tier
        self.cost = cost
        self.image_path = image_path
        self.description = description
        self.have_target = have_target
