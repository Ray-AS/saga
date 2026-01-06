"use server";

import { redirect } from "next/navigation";
import { getStoryStart } from "./mock";

export async function startGame() {
  const { playthroughID } = await getStoryStart();
  redirect(`/game/${playthroughID}`);
}
