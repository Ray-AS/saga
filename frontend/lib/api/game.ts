import {
  toListPlaythroughs,
  toStoryStart,
  toStoryRecap,
  toBackendChoiceWithIntent,
  toStoryAdvance,
  toEnding,
} from "../helpers/convert";
import {
  BackendListPlaythroughsResponse,
  BackendStoryStart,
  BackendStoryAdvance,
  BackendRecap,
  BackendEnding,
} from "../models/backend-types";
import { ChoiceWithIntent } from "../models/types";
import { fetchFromAPI } from "./client";

export async function getPlaythroughList() {
  const data = await fetchFromAPI<BackendListPlaythroughsResponse>("/game");
  return toListPlaythroughs(data.playthroughs);
}

export async function getPlaythrough(id: string) {
  const data = await fetchFromAPI<BackendStoryStart>(`/game/${id}`);
  return toStoryStart(data);
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

export async function advancePlaythrough(id: string, choice: ChoiceWithIntent) {
  const data = await fetchFromAPI<BackendStoryAdvance>(`/game/${id}/choose`, {
    method: "POST",
    body: JSON.stringify(toBackendChoiceWithIntent(choice)),
  });
  return toStoryAdvance(data);
}

export async function getEndingSummary(id: string) {
  const data = await fetchFromAPI<BackendEnding>(`/game/${id}/ending`);
  return toEnding(data);
}
