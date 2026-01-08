import {
  BackendChoiceWithIntent,
  BackendListPlaythroughsResponse,
  BackendStoryStart,
  BackendStoryAdvance,
  BackendPlaythroughSummary,
  BackendRecap,
} from "../models/backend-types";
import {
  ChoiceWithIntent,
  ListPlaythroughs,
  StoryStart,
  StoryAdvance,
  StoryRecap,
} from "../models/types";
import { fetchFromAPI } from "./client";

function toListPlaythroughs(
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

export async function getPlaythroughList() {
  const data = await fetchFromAPI<BackendListPlaythroughsResponse>("/game");
  return toListPlaythroughs(data.playthroughs);
}

function toStoryStart(data: BackendStoryStart): StoryStart {
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

export async function getPlaythrough(id: string) {
  const data = await fetchFromAPI<BackendStoryStart>(`/game/${id}`);
  return toStoryStart(data);
}

function toStoryRecap(data: BackendRecap): StoryRecap {
  return {
    playthroughID: data.playthrough_id,
    story: data.story,
  };
}

export async function getStoryRecap(id: string) {
  const data = await fetchFromAPI<BackendRecap>(`/game/${id}/story`);
  return toStoryRecap(data);
}

export async function deletePlaythrough(id: string) {
  await fetchFromAPI<void>(`/game/${id}`, {
    method: "DELETE",
  });
}

export async function startPlaythrough() {
  const data = await fetchFromAPI<BackendStoryStart>(`/game/start`, {
    method: "POST",
  });
  return toStoryStart(data);
}

function toBackendChoiceWithIntent(
  choice: ChoiceWithIntent,
): BackendChoiceWithIntent {
  return {
    ...choice,
    choice_description: choice.choiceDescription,
  };
}

function toStoryAdvance(data: BackendStoryAdvance): StoryAdvance {
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

export async function advancePlaythrough(id: string, choice: ChoiceWithIntent) {
  const data = await fetchFromAPI<BackendStoryAdvance>(`/game/${id}/choose`, {
    method: "POST",
    body: JSON.stringify(toBackendChoiceWithIntent(choice)),
  });
  return toStoryAdvance(data);
}
