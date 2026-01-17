import Story from "@/components/Story";
// import { getPlaythrough, getStoryRecap } from "@/lib/api/game";
import { getSavedStory, getStoryRecap as getStoryRecapMock } from "@/lib/mocks/mock";

interface GamePageProps {
  params: { id: string };
}

export default async function GamePage({ params }: GamePageProps) {
  const { id } = await params;
  const storySoFar = (await getStoryRecapMock(id)).story;
  const { playthroughID, ...currentTurn } = await getSavedStory(id);
  // const storySoFar = (await getStoryRecap(id)).story;
  // const { playthroughID, ...currentTurn } = await getPlaythrough(id);

  return (
    <>
      <Story
        id={playthroughID}
        initialStory={storySoFar}
        initialTurn={currentTurn}
      />
    </>
  );
}
