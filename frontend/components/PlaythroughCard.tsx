import { PlaythroughSummary } from "@/lib/types";
import PlaythroughNavigateButton from "./PlaythroughNavigateButton";
import PlaythroughDeleteButton from "./PlaythroughDeleteButton";

interface PlaythroughCardProps {
  playthrough: PlaythroughSummary;
}

export default function PlaythroughCard({
  playthrough: p,
}: PlaythroughCardProps) {
  return (
    <div>
      <h3>Playthrough {p.playthroughID}</h3>
      <h4>{p.summary}</h4>
      <h5>
        Act: {p.act} ({p.progress * 100}%)
      </h5>
      {p.canEnd ? <h5>In endgame</h5> : null}
      <PlaythroughNavigateButton id={p.playthroughID} />
      <PlaythroughDeleteButton id={p.playthroughID} />
    </div>
  );
}
