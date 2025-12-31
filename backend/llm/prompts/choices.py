CHOICE_PROMPT = """
Generate 4 distinct choices based on provided story.
Each must:
- Have a clear approach
- Use a Stat: ("force", "guile", "influence", "insight")
- Have realistic Difficulty: ("easy", "medium", "hard", "extreme")

Choice Format:
{{
  "choice_description" (str): "description of choice",
  "difficulty" (Difficulty): "difficulty rating of choice",
  "type" (Stat): "stat that corresponds to choice"
}}

Response must follow this JSON schema:
{{
  "choices" list[Choice]: [Choice 1, Choice 2, Choice 3, Choice 4]
}}

DO NOT return the story along with the choices (Bad: "full": "...", Bad: "condensed": "...")
"""
