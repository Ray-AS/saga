"use client";

import { deletePlaythrough } from "@/lib/mock";

export default function PlaythroughDeleteButton({ id }: { id: string }) {
  async function handleDelete() {
    const { status, response } = await deletePlaythrough(id);
    console.log(status, response.message);
  }

  return (
    <button
      onClick={handleDelete}
      className="w-20 h-8 text-base cursor-pointer shadow-md shadow-black/50 active:translate-y-0.5 active:shadow-zinc-900"
    >
      Delete
    </button>
  );
}
