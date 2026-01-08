import {
  BackendChoiceWithIntent,
  BackendPlaythroughSummary,
  BackendRecap,
  BackendStoryAdvance,
  BackendStoryStart,
} from "../models/backend-types";
import {
  ListPlaythroughs,
  StoryStart,
  StoryRecap,
  ChoiceWithIntent,
  StoryAdvance,
} from "../models/types";

// Convert Python dicts to matching TS Objects

export function toListPlaythroughs(
  data: BackendPlaythroughSummary[],
): ListPlaythroughs {
  return {
    playthroughs: data.map((p) => ({
      playthroughID: p.playthrough_id,
      act: p.act,
      progress: p.progress,
      canEnd: p.can_end,
      summary: p.summary,
    })),
  };
}

export function toStoryStart(data: BackendStoryStart): StoryStart {
  return {
    playthroughID: data.playthrough_id,
    full: data.full,
    condensed: data.condensed,
    choices: data.choices.map((c) => ({
      choiceDescription: c.choice_description,
      difficulty: c.difficulty,
      type: c.type,
    })),
  };
}

export function toStoryRecap(data: BackendRecap): StoryRecap {
  return {
    playthroughID: data.playthrough_id,
    story: data.story,
  };
}

export function toBackendChoiceWithIntent(
  choice: ChoiceWithIntent,
): BackendChoiceWithIntent {
  return {
    ...choice,
    choice_description: choice.choiceDescription,
  };
}

export function toStoryAdvance(data: BackendStoryAdvance): StoryAdvance {
  return {
    playthroughID: data.playthrough_id,
    full: data.full,
    condensed: data.condensed,
    success: data.success,
    choices: data.choices.map((c) => ({
      choiceDescription: c.choice_description,
      difficulty: c.difficulty,
      type: c.type,
    })),
  };
}
