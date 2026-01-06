"use client";

import { useRouter } from "next/navigation";

export default function LoadGameButton() {
  const router = useRouter();

  return (
    <button
      onClick={() => router.push("/game")}
    >
      Load
    </button>
  );
}