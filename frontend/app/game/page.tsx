import PlaythroughCard from "@/components/PlaythroughCard";
import { getPlaythroughList } from "@/lib/mock";
import { startGame } from "@/lib/start";

export default async function GameList() {
  const { playthroughs } = await getPlaythroughList();

  const playthroughElements = playthroughs.map((playthrough, i) => (
    <PlaythroughCard key={i} playthrough={playthrough} />
  ));

  return (
    <>
      <h1>Playthroughs</h1>
      {playthroughElements}
      <form action={startGame}>
        <button type="submit">Start</button>
      </form>
    </>
  );
}
