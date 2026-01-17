import { StatBlock } from "@/lib/models/types";
import { ReactNode } from "react";

export default function StatSummary({ statSummary }: { statSummary: StatBlock }) {
  const statElements: ReactNode[] = [];
    for (const stat of Object.keys(statSummary) as (keyof StatBlock)[]) {
      statElements.push(
        <div>
          {stat.charAt(0).toUpperCase() + stat.slice(1)}: {statSummary[stat]}
        </div>,
      );
    }

  return (
    <section className="mx-4 mb-10 p-6 shadow-lg shadow-neutral-950">
      <header className="text-xl font-bold">The Measure of You</header>
      {statElements}
    </section>
  )
}