from logger import logger


class World:
    def __init__(self, location, time):
        self.location = location
        self.time = time
        # list of dicts
        # { description, location, time, characters_involved? }
        self.events = []
        # list of dicts
        # { name, background }
        self.npcs = []

    def add_event(self, description, characters_involved):
        new_event = {
            'description': description,
            'location': self.location,
            'time': self.time,
            'characters_involved': characters_involved,
        }
        logger.log_event_added(new_event)
        self.events.append(new_event)

    def add_npc(self, name, background):
        new_npc = {'name': name, 'background': background}
        logger.log_npc_added(new_npc)
        self.npcs.append(new_npc)


# arda = World('Middle Earth', '3000 CE')
# arda.add_event('The one ring is destroyed.', ['Gandalf', 'Frodo', 'Sam'])
