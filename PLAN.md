# Saga

An AI-powered choose your own adventure simulator.

## Gameplay

- Success Grade
  - Indicator of the chance of success for each choice
  - Base Uncertainty + Stats + Intent
- Stats
  - Influence: social status, persuasion, intimidation, reputation
  - Guile: stealth, deception, misdirection
  - Force: physical prowess, endurance, violence
  - Insight: perception, reasoning, intuition
  - Start at 0
  - Creation of character (llm gives a few formative choices) give +1 maybe + 2 boosts to specific stats
    - Early game play style
  - Milestone improvement (i.e. 8 successes -> +1 to stat)
- Flags
  - Player State: injured, exhausted
  - Exposure State: exposed, pursued
  - Social State: hostile npc, social locked
  - Pressure State: time pressure, endgame
- Tension Pool
  - One global long-term variable that affects the story
  - States: low, med, high, etc tension levels
  - Limited choices and more pressure
- Risk
  - desperate, bold, standard, careful
  - affects probability of success and quality of reward
- Act Score
  - Long term variable to track state of story to ensure constant forward momentum
  - 1: establish world and characters; introduce main conflict
  - 2: learn about conflict and villain; introduce a twist of revelation
  - 3: culminate in a satisfying final sequence/confrontation; no new plots; resolve story
  - 4: epilogue describing world and characters and other things based on user choices

- Future
  - Character customization
  - More interactive gameplay elements outside of choices

## Features

- React/Typescript front end
  - Main menu
    - Start (Pick length; genre; difficulty; etc)
    - Load (Saves?)
    - Settings (Art style; visual)
    - Stats
  - Game
    - Character section
    - Story box
    - Choices
    - Save
    - Quit
  - End screen
    - Stats
- Node/Express/Typescript/
  - Parse player actions
  - Engineer AI prompts
  - Call model
  - Save to database
  - Return story progression
- Database (MongoDB or Postgres)
  - Player/user data (+ world data for user)
  - Sessions
  - Segments
- AI Images?
- Testing
  - Unit testing w/ Vitest
  - Integration testing?
  - E2E?

## Additional

- Player classes / stats that evolve
- NPCs controlled by AI
- Reading text

## Game Loop

- Start game
  - Choose length, genre, difficulty
  - Create character (spells, stats, etc.)
    - For now, have very basic predefined characters
- Story introduction
- Game loop
  - Description
  - Choices (success/failure chance based on stats)
  - Reaction from game engine
  - Update game state (world, npc, character, story data) -> Save point?
  - Repeat
- End game
  - Summary screen
- Dynamic story generation + strict, rule-based combat
  - Choices are dynamically-generated (success on some choices can depend on player stats i.e. DC)
  - Combat enemies are dynamically-generated in a structured way (hp, damage, etc.)
  - Player interaction in combat is rule-based i.e. predefined spells and attacks
    - D&D style combat may not be the best fit
    - Puzzles?
    - Cards?

## Classes

- Character
  - Stats (e.g. health)
  - Abilities
- World
  - Location
  - Time
  - Key data (for ai context) (e.g. bosses, cities)
  - NPCs (basic list of NPCs with a very little bit of context)
- Playthrough
  - Difficulty/genre/length
  - World state
  - Character state
  - Story history
  - Game progress/Game over?
- Story engine
  - Received structured context (character / world / story so far)
  - Generates structured output ( story update / consequences / choices)
  - Validation of output
- Game engine
  - Gets and evaluates player choice
  - Success vs. failure
  - Updates playthrough data
  - Decides if game is ended
  - Talks to story generator

## Basic Start

- Character
  - Just a name
- World
  - Tracking events
  - Location
  - Tracking npcs
- Storyteller
  - Generate story based on user choice
  - Prompt; history; example/format
- Playthrough
  - Game settings (genre, length)
  - Hold world and character
  - Hold unabridged story
  - Check progress
  - Generate assets/objects
