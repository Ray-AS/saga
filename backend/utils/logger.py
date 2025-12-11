from models import NPC, Event


class Logger:
    def __init__(self):
        pass

    def log_dmg_taken(self, name: str, dmg: int, current_hp: int):
        print(f'{name} taking {dmg} damage. HP: {current_hp - dmg}')

    def log_heal(self, name: str, amount: int, current_hp: int):
        print(f'{name} healing {amount} hp. HP: {current_hp + amount}')

    def log_dmg_done(
        self, name: str, target_name: str, attack_dmg: int, target_hp: int
    ):
        print(
            f'{name} dealing {attack_dmg} damage to {target_name}. Target HP: {target_hp - attack_dmg}'
        )

    def log_event_added(self, new_event: Event):
        print(
            f'EVENT ({new_event["location"]}): '
            f'{new_event["description"]} {new_event["characters_involved"]}'
        )

    def log_npc_added(self, new_npc: NPC):
        print(f'NPC ({new_npc["name"]}): {new_npc["background"]}')

    def log_world_generated(self, name: str):
        print(f'WORLD CREATED ({name})')


logger = Logger()
