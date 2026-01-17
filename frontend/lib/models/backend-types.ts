import { Difficulty, Intent, Stat, StatBlock, Success } from "./types";

export type BackendPlaythroughSummary = {
  readonly playthrough_id: string;
  readonly act: "SETUP" | "ESCALATION" | "RESOLUTION";
  readonly progress: number;
  readonly can_end: boolean;
  readonly summary: string;
};

export type BackendListPlaythroughsResponse = {
  readonly playthroughs: BackendPlaythroughSummary[];
};

interface BackendChoice {
  readonly choice_description: string;
  readonly difficulty: Difficulty;
  readonly type: Stat;
}

export interface BackendChoiceWithIntent extends BackendChoice {
  readonly intent: Intent;
}

export interface BackendStoryStart {
  readonly playthrough_id: string;
  readonly full: string;
  readonly condensed: string;
  readonly choices: BackendChoice[];
}

export interface BackendStoryAdvance extends BackendStoryStart {
  readonly success: Success;
}

export interface BackendRecap {
  readonly playthrough_id: string;
  readonly story: string[];
}

export interface BackendEnding {
  readonly playthrough_summary: string
  readonly character_summary: string
  readonly stat_summary: StatBlock
}