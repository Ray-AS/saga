from textwrap import dedent

from groq.types.chat import ChatCompletionMessageParam as Message

MODEL_LIST = [
    'llama-3.3-70b-versatile',
    #'llama-3.1-8b-instant',
    'openai/gpt-oss-120b',
    #'openai/gpt-oss-20b',
]

ROLE_DESCRIPTION = 'You are the story teller of an interactive story.'

STYLE_CONSTRAINTS = [
    'Output strictly valid JSON in the exact format matching the schema: {"full": "...", "condensed": "...", "choices": [{...}]}. No text before or after the JSON object',
    "The response must begin with '{' and end with '}'. Do not include any text outside the JSON object.",
    'Escape double quotes with a backslash if they appear inside a string.',
    'DO NOT include a "choices: ..." section in the "full" value of the object.',
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

CHOICE_SCHEMA: str = dedent("""
Stats:
- Force: physical prowess; endurance; violence
- Guile: stealth; deception; misdirection
- Influence: social status; persuasion; intimidation
- Insight: perception; reasoning; intuition

A choice (of type Choice) follows this format:
{
    "choice" (str): "description for an option the player can choose; ensure a little description (bad: "defend", good: "unsheathe your blade and parry the strike")",
    "difficulty" ("easy" | "medium" | "hard" | "extreme"): "the difficulty of the choice; be realistic (e.g. generally, assassinate king shouldn't be "easy")",
    "type" ("force" | "guile" | "influence" | "insight"): "classification of choice for a stat based on what it requires"
}
""").strip()

FORMAT: str = dedent("""
Construct your response as a single, valid JSON object following this schema:
{
    "full" (str): "entire description of events (150-300 words; longer for important scenes, shorter for unimportant)",
    "condensed" (str): "short description of events; keep only essentials that affect future story logic (50-100 words / 3-4 sentences)",
    "choices" (list[Choice]]): "available options for the player to proceed; must be unique and make sense for the narrative (e.g. [{"choice": "option 1", "difficulty": "easy", "type": "force"}, ...])"
}
""").strip()

PROGRESSION_DESCRIPTION = """A single response represents exactly one turn:
- Resolve the player's last choice
- Update the world state
- Present new choices
- Do not resolve any future choices"""

STARTING_PROMPT: Message = {
    'role': 'user',
    'content': 'Generate the opening scene of a new interactive story.',
}
