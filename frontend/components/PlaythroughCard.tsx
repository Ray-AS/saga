import { PlaythroughSummary } from "@/lib/models/types";
import PlaythroughNavigateButton from "./PlaythroughNavigateButton";
import PlaythroughDeleteButton from "./PlaythroughDeleteButton";

interface PlaythroughCardProps {
  playthrough: PlaythroughSummary;
}

export default function PlaythroughCard({
  playthrough: p,
}: PlaythroughCardProps) {
  return (
    <div className="flex h-70 w-80 flex-col gap-2 p-4 shadow-lg/50 shadow-neutral-950">
      <div className="text-lg">Playthrough {p.playthroughID}</div>
      <div className="text-sm">{p.summary}</div>
      <div>
        Act: {p.act} ({p.progress * 100}%)
      </div>
      {p.canEnd ? <div>In endgame</div> : null}
      <div className="mt-auto flex w-full justify-between">
        <PlaythroughNavigateButton id={p.playthroughID} />
        <PlaythroughDeleteButton id={p.playthroughID} />
      </div>
    </div>
  );
}
