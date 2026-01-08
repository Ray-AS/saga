import { BackendListPlaythroughsResponse, BackendPlaythroughBasic, BackendPlaythroughSummary, BackendRecap } from "../models/backend-types";
import { ListPlaythroughs, PlaythroughBasic, StoryRecap } from "../models/types";
import { fetchFromAPI } from "./client";

function toListPlaythroughs(data: BackendPlaythroughSummary[]): ListPlaythroughs {
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


function toPlaythroughBasic(data: BackendPlaythroughBasic): PlaythroughBasic {
  return {
    playthroughID: data.playthrough_id,
    full: data.full,
    condensed: data.condensed,
    choices: data.choices.map(c => ({
      choiceDescription: c.choice_description,
      difficulty: c.difficulty,
      type: c.type,
    })),
  };
}

export async function getPlaythrough(id: string) {
  const data = await fetchFromAPI<BackendPlaythroughBasic>(`/game/${id}`);
  return toPlaythroughBasic(data);
}

function toStoryRecap(data: BackendRecap): StoryRecap {
  return {
    playthroughID: data.playthrough_id,
    story: data.story
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
  const data = await fetchFromAPI<BackendPlaythroughBasic>(`/game/start`, {
    method: "POST",
  });
  return toPlaythroughBasic(data);
}