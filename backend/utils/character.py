from logger import logger


class Character:
    def __init__(self, name, character_class):
        self.name = name
        self.character_class = character_class
        self.hp = 100
        self.attack_dmg = 10

    def take_dmg(self, dmg):
        logger.log_dmg_taken(self.name, dmg, self.hp)
        self.hp -= dmg

    def heal(self, amount):
        logger.log_heal(self.name, amount, self.hp)
        self.hp += amount

    def attack_target(self, target):
        logger.log_dmg_done(self.name, target.name, self.attack_dmg, target.hp)
        target.take_dmg(self.attack_dmg)


# gandalf = Character('Gandalf', 'Wizard')
# gandalf.take_dmg(15)
