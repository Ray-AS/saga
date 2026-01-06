import PlaythroughCard from "@/components/PlaythroughCard";
import StartGameButton from "@/components/StartGameButton";
import { getPlaythroughList } from "@/lib/mock";

export default async function GameList() {
  const { playthroughs } = await getPlaythroughList();

  const playthroughElements = playthroughs.map((playthrough, i) => (
    <PlaythroughCard key={i} playthrough={playthrough} />
  ));

  return (
    <main className="flex flex-col justify-center items-center gap-8">
      <StartGameButton />
      <section className="max-w-xl flex flex-wrap gap-8 justify-center">
        {playthroughElements}
      </section>
    </main>
  );
}
