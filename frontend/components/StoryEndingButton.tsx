"use client";

import { useRouter } from "next/navigation";

export default function StoryEndingButton({ id }: { id: string }) {
  const router = useRouter();

  const viewPlaythroughOutcome = () => {
    router.push(`/game/${id}/ending`);
  };

  return (
    <button
      onClick={viewPlaythroughOutcome}
      className="h-8 w-20 cursor-pointer text-base shadow-md shadow-black/75 transition hover:bg-neutral-800 active:translate-y-0.5 active:shadow-black/20"
    >
      View the Aftermath of Your Saga
    </button>
  );
}