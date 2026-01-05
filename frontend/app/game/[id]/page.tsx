import Story from "@/components/Story";
import { getSavedStory, getStoryRecap } from "@/lib/mock";

interface GamePageProps {
  params: { id: string };
}

export default async function GamePage({ params }: GamePageProps) {
  const storySoFar = (await getStoryRecap(params.id)).story;
  const { playthroughID, ...currentTurn } = await getSavedStory(params.id);

  return (
    <>
      <h1>Playthrough</h1>
      <Story
        id={playthroughID}
        initialStory={storySoFar}
        initialTurn={currentTurn}
      />
    </>
  );
}
