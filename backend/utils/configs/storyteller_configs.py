from textwrap import dedent

from groq.types.chat import ChatCompletionMessageParam as Message

MODEL_LIST = [
    'llama-3.3-70b-versatile',
    #'llama-3.1-8b-instant',
    'openai/gpt-oss-120b',
    #'openai/gpt-oss-20b',
]

# GENERAL PROMPTS
ROLE_DESCRIPTION = 'You are the story teller of an interactive story.'

STYLE_CONSTRAINTS = [
    'Output strictly valid JSON in the exact format matching the schema: {"full": "...", "condensed": "...", "choices": [{...}]}. No text before or after the JSON object',
    "The response must begin with '{' and end with '}'. Do not include any text outside the JSON object.",
    'Escape double quotes with a backslash if they appear inside a string.',
    'DO NOT include a "choices: ..." section in the "full" value of the object.',
    'DO NOT summarize previous context; assume that was described adequately in previous interactions.'
    "Write exclusively in second person, always referring to the player as 'you'.",
    "The 'full' field must contain only immersive narrative prose. Do not include summaries, labels, or meta commentary.",
    'Use concrete sensory details (sound, texture, temperature, smell) instead of abstract or vague concepts.',
    "Avoid generic fantasy phrases (e.g., 'dark energy', 'malevolent presence', 'ancient power').",
    'Keep prose vivid, concise, and actionable; every paragraph should move the situation forward.',
    'Vary sentence length intentionally to control pacing and tension.',
    'End each scene with a clear, natural consequence embedded in the narrative (not a labeled summary).',
    "Do not summarize consequences using labels like 'Outcome:' or 'Result:'. Consequences must be embedded naturally in the narrative.",
]

ACTION_CONSTRAINTS = [
    "Never control the player character. Describe only the consequences of the player's chosen action.",
    'If you accidentally violate player agency or describe unchosen outcomes, you MUST immediately rewrite the response to fix the issue before replying.'
    # 'Ensure outcomes are unbiased and realistic. Success is not guaranteed; failure and neutral results must occur when justified.',
    'Every scene must have a clear objective. Once it is achieved or failed, end the scene and transition.',
    # 'If the player repeats the same type of action more than twice, force a decisive change (success, failure, or irreversible consequence).',
    'NPCs must have conflicting motivations, limited knowledge, and persistent attitudes that change based on player actions.',
    'All player actions must have tangible costs or tradeoffs.',
    'Each choice must meaningfully change the world state. Do not offer choices that lead to the same result.',
    'The world advances even if the player hesitates. Delays increase danger, remove options, or worsen outcomes.',
    'When presenting choices, describe only the immediate intent or approach. Never reveal results in advance.',
    'Never describe the consequences of an unchosen option. Consequences are revealed only after the player commits.',
    "After resolving the player's chosen action, stop. Do not advance the story beyond the immediate consequences.",
]

# STORY ADVANCEMENT PROMPTS
CHOICE_SCHEMA: str = dedent("""
Stats:
- Force: physical prowess; endurance; violence
- Guile: stealth; deception; misdirection
- Influence: social status; persuasion; intimidation
- Insight: perception; reasoning; intuition

A choice (of type Choice) follows this format:
{
    "choice_description" (str): "description for an option the player can choose; ensure a little description (bad: "defend", good: "unsheathe your blade and parry the strike")",
    "difficulty" ("easy" | "medium" | "hard" | "extreme"): "the difficulty of the choice; be realistic (e.g. generally, assassinate king shouldn't be "easy")",
    "type" ("force" | "guile" | "influence" | "insight"): "classification of choice for a stat based on what it requires"
}
""").strip()

FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    "full" (str): "entire description of events (150-300 words; longer for important scenes, shorter for unimportant)",
    "condensed" (str): "short description of events; keep only essentials that affect future story logic (50-100 words / 3-4 sentences)",
    "choices" (list[Choice]]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. [{"choice_description": "option 1", "difficulty": "easy", "type": "force"}, ...])"
}
""").strip()

PROGRESSION_DESCRIPTION = """A single response represents exactly one turn:
- Resolve the player's last choice
- Update the world state
- Present new choices
- Do not resolve any future choices"""

# STORY START PROMPT
STARTING_PROMPT: Message = {
    'role': 'user',
    'content': 'Generate the opening scene of a new interactive story.',
}

# CHARACTER CREATION PROMPTSs
CHOICE_SCHEMA: str = dedent("""
Description Categories:
- Force: physical prowess; endurance; violence
- Guile: stealth; deception; misdirection
- Influence: social status; persuasion; intimidation
- Insight: perception; reasoning; intuition

A choice (of type Choice) follows this format:
{
    "choice_description" (str): "description for an option the player can choose; ensure a little description (bad: "defend", good: "unsheathe your blade and parry the strike")",
    "type" ("force" | "guile" | "influence" | "insight"): "classification of choice as to what it would say about the character"
}
""").strip()

STAT_FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    "full" (str): "entire description of events (~300 words)",
    "condensed" (str): "short description of events; keep only essentials that affect future story logic (150 words / 3-6 sentences)",
    "choices" (list[Choice]]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. [{"choice_description": "option 1", "type": "force"}, ...])"
}
""").strip()

STAT_PROMPT = f"""This scenario is a short, self-contained character creation arc.
- The entire arc must resolve cleanly within 4 interactions total.
- Try to make the arc's story unique (i.e. no child being cornered by wolves)
- Each interaction represents a formative moment in the character's past.
- Do not introduce new plots outside this mini-arc, but allow consequences and reactions from prior choices to carry forward naturally.
- This arc must feel complete and conclusive by the final interaction.

Progression expectations:
- Early interactions (1): establish background, temperament, and instincts.
- Middle interactions (2-3): test values, force tradeoffs, or reveal flaws.
- Final interaction (4): should be a culminating moment and morally gray, where the player truly needs to think
- Resolution: describe the results of the player's final choice and end the mini-arc in a satisfying way without leaving any hanging threads

Final interaction rules:
- Choices should feel decisive and identity-defining.
- The narrative should naturally conclude the formative experience.
- The outcome should feel like a foundation for the main story, not its beginning.

{CHOICE_SCHEMA}

{STAT_FORMAT}

- DO NOT describe the choices "full" section of the response (that's what the "choices" section is for); instead, only describe the story and outcomes based on previous choice; Bad examples:
    - "You stand at a crossroads: do you secure the village further, investigate the source of the wolves' desperation, or seize the brief calm for your own needs?"
    - "The decision now rests on how you will address the obstructed road, shaping how the village will see you in the hours to come."
- DO NOT describe the player character's personality (the game engine will determine that); only describe reactions by the environment/npcs to the player character's decisions
- ALWAYS progress the story based on the players last choice.
- DO NOT summarize previous context; assume that was adequately achieved in previous interactions
"""
