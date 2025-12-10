class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.hp = 100
        self.attack_dmg = 10

    def take_dmg(self, dmg):
        self.hp -= dmg

    def heal(self, amount):
        self.hp += amount

    def attack_target(self, target):
        target.take_dmg(self.attack_dmg)
