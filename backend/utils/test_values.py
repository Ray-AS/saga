from models import Response, Turn

test_history: list[Turn] = [
    {
        'user': 'use mace to attack goblin',
        'ai': 'goblin reels back in pain, then retaliates with its claws.',
    },
    {
        'user': 'finish the goblin off using a fireball spell',
        'ai': 'the goblin is no more, leaving behind only the ashes of its corpse.',
    },
    {
        'user': 'release the captives from their cage',
        'ai': 'the captives, who believed there was no escape, are eternally grateful to you.',
    },
]

mock_responses: list[Response] = [
    {
        'full': 'As you escort the captives back to town, they share tales of their captivity and the brutal treatment they suffered at the hands of the goblins. The townspeople, upon seeing the freed captives, erupt in cheers and celebration. The town elder approaches you, his eyes filled with gratitude, and thanks you for your bravery. However, amidst the festivities, you notice a figure watching from the shadows, their intentions unclear. The captives, now safe, thank you for your selflessness and assure you that they will never forget your heroism.',
        'condensed': 'Escorted captives back to town, received praise',
        'key': 'Freed captives, returned to town',
        'characters': [
            {'name': 'Town Elder', 'action': 'Thanked you for bravery'},
            {'name': 'Mysterious Figure', 'action': 'Watched from shadows'},
            {'name': 'Captives', 'action': 'Thanked you for rescue'},
        ],
        'choices': [
            'Approach the mysterious figure',
            'Celebrate with the townspeople',
            'Meet with the town elder to discuss further adventures',
        ],
    },
    {
        'full': "As you escort the captives back to town, they thank you profusely for saving their lives. The villagers, who had given up hope of ever seeing their loved ones again, rejoice at their return. The village elder approaches you, tears in his eyes, and offers a reward for your bravery. However, amidst the celebration, a stranger lurks in the shadows, watching you with an intent gaze. The villagers seem oblivious to the stranger's presence, but you sense that something is amiss.",
        'condensed': 'Escorted captives back to town, received thanks and reward, stranger lurks',
        'key': 'Returned captives to town, stranger appears',
        'characters': [
            {'name': 'Village Elder', 'action': 'Offered a reward for bravery'},
            {'name': 'Stranger', 'action': 'Lurking in the shadows, watching you'},
        ],
        'choices': [
            'Accept the reward and celebrate with the villagers',
            'Approach the stranger and demand to know their intentions',
            'Decline the reward, feeling that your actions were just',
        ],
    },
    {
        'full': "As you escort the captives back to town, they share tales of their ordeal and the goblin's lair, warning of potential dangers that may still lurk within. The townspeople, overjoyed by the captives' return, gather to celebrate and thank you for your bravery. However, amidst the festivities, a concerned villager approaches you, speaking of strange occurrences and eerie feelings that have been plaguing the town lately. The villager leans in closer, whispering about an abandoned mine on the outskirts of town, where the strange happenings seem to originate.",
        'condensed': 'Escorted captives back to town, learned of strange occurrences',
        'key': 'Returned captives to town',
        'characters': [
            {'name': 'Villager', 'action': 'Approached you with concerns'},
            {'name': 'Captives', 'action': 'Shared tales of their ordeal'},
        ],
        'choices': [
            'Investigate the abandoned mine',
            'Join the celebration and rest',
            'Seek out the town elder for more information',
        ],
    },
]
