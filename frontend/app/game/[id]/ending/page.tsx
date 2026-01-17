import { getEndingSummary } from "@/lib/api/game";
import { StatBlock } from "@/lib/models/types";
import { ReactNode } from "react";

interface EndingPageProps {
  params: { id: string };
}

export default async function EndingPage({ params }: EndingPageProps) {
  const { id } = await params;
  const { playthrough, character, stats } = await getEndingSummary(id);

  const statElements: ReactNode[] = [];
  for (const stat of Object.keys(stats) as (keyof StatBlock)[]) {
    statElements.push(
      <div>
        {stat}: {stats[stat]}
      </div>,
    );
  }

  return (
    <main>
      <div>Who you were: {character}</div>
      <div>What became of your world:</div>
      <p>{playthrough}</p>
      <div>
        <div>Your stats:</div>
        {statElements}
      </div>
    </main>
  );
}
