"use client";

import { useRouter } from "next/navigation";

export default function LoadGameButton() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/game")}
      className="w-32 h-10 text-xl cursor-pointer shadow-md shadow-black/50 active:translate-y-0.5 active:shadow-zinc-900"
    >
      Load
    </button>
  );
}