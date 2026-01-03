enum Difficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
  EXTREME = 'extreme',
}

enum Stat {
  FORCE = 'force',
  GUILE = 'guile',
  INFLUENCE = 'influence',
  INSIGHT = 'insight',
}

enum Intent {
  CAREFUL = 'careful',
  STANDARD = 'standard',
  BOLD = 'bold',
  DESPERATE = 'desperate',
}

enum Success{
  C_FAIL = 'CRITICAL FAILURE',
  FAIL = 'FAILURE',
  PARTIAL = 'PARTIAL SUCCESS',
  SUCCESS = 'SUCCESS',
  C_SUCCESS = 'CRITICAL SUCCESS',
}

interface Choice {
  readonly choiceDescription: string
  readonly difficulty: Difficulty
  readonly type: Stat
}

interface PlaythroughSummary {
  readonly playthroughID: string
  readonly act: string
  readonly progress: number
  readonly canEnd: boolean
  readonly summary: string
}

export interface ChoiceInfo extends Choice {
  intent: Intent
}

export interface StoryStart {
  readonly playthroughID: string
  readonly full: string
  readonly condensed: string
  readonly choices: Choice[]
}

export interface StoryAdvance extends StoryStart {
  readonly success: Success
}

export interface ListPlaythroughs {
  readonly playthroughs: PlaythroughSummary[]
}