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
    <div className="w-50 flex flex-col gap-2 items-center">
      <div className="text-lg">Playthrough {p.playthroughID}</div>
      <div>{p.summary}</div>
      <div>
        Act: {p.act} ({p.progress * 100}%)
      </div>
      {p.canEnd ? <div>In endgame</div> : null}
      <div className="w-full flex justify-between">
        <PlaythroughNavigateButton id={p.playthroughID} />
        <PlaythroughDeleteButton id={p.playthroughID} />
      </div>
    </div>
  );
}
