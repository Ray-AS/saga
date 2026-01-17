export default function TextSummary({summaryHeader, summary}: {summaryHeader: string, summary: string}) {
  return (
    <section className="mx-4 mb-10 p-6 shadow-lg shadow-neutral-950">
      <header className="text-xl font-bold">{summaryHeader}</header>
      <div>{summary}</div>
    </section>
  )
}