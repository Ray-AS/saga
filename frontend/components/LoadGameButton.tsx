"use client";

import { useRouter } from "next/navigation";

export default function LoadGameButton() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/game")}
      className="h-10 w-32 cursor-pointer text-xl shadow-md shadow-black/75 transition hover:bg-neutral-800 active:translate-y-0.5 active:shadow-black/20"
    >
      Load
    </button>
  );
}
