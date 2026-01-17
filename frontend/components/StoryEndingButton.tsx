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
      className="text-center my-2 w-full cursor-pointer px-5 py-3 shadow-md shadow-black/75 transition hover:bg-neutral-800 hover:shadow-black/60 active:translate-y-0.5 active:shadow-black/20"
    >
      View the echoes of your Saga
    </button>
  );
}