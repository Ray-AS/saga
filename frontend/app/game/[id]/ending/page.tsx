import StatSummary from "@/components/StatSummary";
import TextSummary from "@/components/TextSummary";
import { getEndingSummary } from "@/lib/api/game";

interface EndingPageProps {
  params: { id: string };
}

export default async function EndingPage({ params }: EndingPageProps) {
  const { id } = await params;
  const { playthrough, character, stats } = await getEndingSummary(id);

  return (
    <main>
      <TextSummary summaryHeader={"Who You Became"} summary={character} />
      <TextSummary summaryHeader={"The World You Left Behind"} summary={playthrough} />
      <StatSummary statSummary={stats} />
    </main>
  );
}
