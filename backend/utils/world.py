from logger import logger
from models import Event, NPC


class World:
    def __init__(self, location: str, time: str):
        self.location = location
        self.time = time
        # list of dicts
        # { description, location, time, characters_involved? }
        self.events: list[Event] = []
        # list of dicts
        # { name, background }
        self.npcs: list[NPC] = []

    def add_event(self, description: str, characters_involved: list[str]):
        new_event: Event = {
            'description': description,
            'location': self.location,
            'time': self.time,
            'characters_involved': characters_involved,
        }
        logger.log_event_added(new_event)
        self.events.append(new_event)
        return new_event

    def add_npc(self, name: str, background: str):
        new_npc: NPC = {'name': name, 'background': background}
        logger.log_npc_added(new_npc)
        self.npcs.append(new_npc)
        return new_npc


# arda = World('Middle Earth', '3000 CE')
# arda.add_event('The one ring is destroyed.', ['Gandalf', 'Frodo', 'Sam'])
