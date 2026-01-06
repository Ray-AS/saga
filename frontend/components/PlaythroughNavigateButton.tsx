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
      className="w-20 h-8 text-base cursor-pointer shadow-md shadow-black/50 active:translate-y-0.5 active:shadow-zinc-900"
    >
      Resume
    </button>
  );
}
