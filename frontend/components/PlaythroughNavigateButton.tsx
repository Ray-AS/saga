"use client";

import { useRouter } from "next/navigation";

export default function PlaythroughNavigateButton({ id }: { id: string }) {
  const router = useRouter();

  const resumePlaythrough = () => {
    router.push(`/game/${id}`);
  };

  return (
    <button
      onClick={resumePlaythrough}
      className="h-8 w-20 cursor-pointer text-base shadow-md shadow-black/75 transition hover:bg-neutral-800 active:translate-y-0.5 active:shadow-black/20"
    >
      Resume
    </button>
  );
}
