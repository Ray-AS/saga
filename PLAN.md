# Saga

An AI-powered choose your own adventure simulator.

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
