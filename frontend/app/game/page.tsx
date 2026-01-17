import PlaythroughCard from "@/components/PlaythroughCard";
import StartGameButton from "@/components/StartGameButton";
import { getPlaythroughList } from "@/lib/api/game";
// import { getPlaythroughList as getPlaythroughListMock } from "@/lib/mocks/mock";

export default async function GameList() {
  // const { playthroughs } = await getPlaythroughListMock();
  const { playthroughs } = await getPlaythroughList();

  const playthroughElements = playthroughs.map((playthrough, i) => (
    <PlaythroughCard key={i} playthrough={playthrough} />
  ));

  return (
    <main className="flex flex-col items-center justify-center gap-8">
      <StartGameButton />
      <section className="flex max-w-3xl flex-wrap justify-center gap-8">
        {playthroughElements}
      </section>
    </main>
  );
}
