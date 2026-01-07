import { Difficulty, Stat } from "./types";

export type BackendPlaythroughSummary = {
  playthrough_id: string;
  act: "SETUP" | "ESCALATION" | "RESOLUTION";
  progress: number;
  can_end: boolean;
  summary: string;
};

export type BackendListPlaythroughsResponse = {
  playthroughs: BackendPlaythroughSummary[];
};

interface BackendChoice {
  choice_description: string;
  difficulty: Difficulty;
  type: Stat;
}

export interface BackendPlaythroughBasic {
  playthrough_id: string;
  full: string
  condensed: string
  choices: BackendChoice[]
}

export interface BackendRecap {
  playthrough_id: string;
  story: string[];
}