import Story from "@/components/Story";
import { getSavedStory, getStoryRecap } from "@/lib/mock";

export default async function GamePage() {
  const storySoFar = (await getStoryRecap()).story;
  const { playthroughID, ...currentTurn } = await getSavedStory();

  return (
    <>
      <h1>Playthrough</h1>
      <Story id={playthroughID} initialStory={storySoFar} initialTurn={currentTurn} />
    </>
  );
}
