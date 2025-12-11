from logger import logger


class Character:
    def __init__(self, name: str, character_class: str):
        self.name = name
        self.character_class = character_class
        self.hp: int = 100
        self.attack_dmg: int = 10

    def take_dmg(self, dmg: int):
        logger.log_dmg_taken(self.name, dmg, self.hp)
        self.hp -= dmg
        return self.hp

    def heal(self, amount: int):
        logger.log_heal(self.name, amount, self.hp)
        self.hp += amount
        return self.hp

    def attack_target(self, target: 'Character'):
        logger.log_dmg_done(self.name, target.name, self.attack_dmg, target.hp)
        target.take_dmg(self.attack_dmg)
        return target.hp


# gandalf = Character('Gandalf', 'Wizard')
# gandalf.take_dmg(15)
