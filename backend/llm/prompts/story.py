STORY_PROMPT_START = """
Generate story

Respond with immersive prose only. Response must follow this JSON schema:
{{
  "full" (str): "complete description of story progression (200-300 words)",
  "condensed" (str): "shorter description of event and key points (~100 words)"
}}
"""

STORY_PROMPT_TURN = """
Resolve the player's action.

Metadata:
Action: {action}
Success: {success}
Intent: {intent}

Respond with immersive prose only. Response must follow this JSON schema:
{{
  "full" (str): "complete description of story progression (200-300 words)",
  "condensed" (str): "shorter description of event and key points (~100 words)"
}}
"""
