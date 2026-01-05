export enum Difficulty {
  EASY = 'easy',
  MEDIUM = 'medium',
  HARD = 'hard',
  EXTREME = 'extreme',
}

export enum Stat {
  FORCE = 'force',
  GUILE = 'guile',
  INFLUENCE = 'influence',
  INSIGHT = 'insight',
}

export enum Intent {
  CAREFUL = 'careful',
  STANDARD = 'standard',
  BOLD = 'bold',
  DESPERATE = 'desperate',
}

export enum Success{
  C_FAIL = 'CRITICAL FAILURE',
  FAIL = 'FAILURE',
  PARTIAL = 'PARTIAL SUCCESS',
  SUCCESS = 'SUCCESS',
  C_SUCCESS = 'CRITICAL SUCCESS',
}

export interface Choice {
  readonly choiceDescription: string
  readonly difficulty: Difficulty
  readonly type: Stat
}

export interface PlaythroughSummary {
  readonly playthroughID: string
  readonly act: "SETUP" | "ESCALATION" | "RESOLUTION"
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

export type StoryWithoutID = Omit<StoryStart, "playthroughID">

export interface StoryAdvance extends StoryStart {
  readonly success: Success
}

export interface StoryRecap {
  readonly playthroughID: string
  readonly story: string[]
}

export interface ListPlaythroughs {
  readonly playthroughs: PlaythroughSummary[]
}