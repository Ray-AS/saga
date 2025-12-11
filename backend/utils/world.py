from logger import logger
from models import NPC, Event


class World:
    def __init__(self, name: str, location: str):
        self.name = name
        self.location = location
        # list of dicts
        # { description, location, time, characters_involved? }
        self.events: list[Event] = []
        # list of dicts
        # { name, background }
        self.npcs: list[NPC] = []

    def add_event(self, description: str, characters_involved: list[str] | None = None):
        new_event: Event = {
            'description': description,
            'location': self.location,
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
