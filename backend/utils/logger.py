class Logger:
    def __init__(self):
        pass

    def log_dmg_taken(self, name, dmg, current_hp):
        print(f'{name} taking {dmg} damage. HP: {current_hp - dmg}')

    def log_heal(self, name, amount, current_hp):
        print(f'{name} healing {amount} hp. HP: {current_hp + amount}')

    def log_dmg_done(self, name, target_name, attack_dmg, target_hp):
        print(
            f'{name} dealing {attack_dmg} damage to {target_name}. Target HP: {target_hp - attack_dmg}'
        )

    def log_event_added(self, new_event):
        print(
            f'EVENT ({new_event["location"]} at {new_event["time"]}): '
            f'{new_event["description"]} {new_event["characters_involved"]}'
        )

    def log_npc_added(self, new_npc):
        print(f'NPC ({new_npc["name"]}): {new_npc["background"]}')


logger = Logger()
