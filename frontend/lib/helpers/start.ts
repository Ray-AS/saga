"use server";

import { redirect } from "next/navigation";
import { startPlaythrough } from "../api/game";
// import { getStoryStart } from "./mocks/mock";

export async function startGame() {
  // const { playthroughID } = await getStoryStart();
  const { playthroughID } = await startPlaythrough();
  redirect(`/game/${playthroughID}`);
}
