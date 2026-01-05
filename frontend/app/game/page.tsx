import PlaythroughCard from "@/components/PlaythroughCard";
import { getPlaythroughList } from "@/lib/mock";

export default async function GameList() {
  const { playthroughs } = await getPlaythroughList();

  const playthroughElements = playthroughs.map((playthrough, i) => (
    <PlaythroughCard key={i} playthrough={playthrough} />
  ));

  return (
    <>
      <h1>Playthroughs</h1>
      {playthroughElements}
    </>
  );
}
