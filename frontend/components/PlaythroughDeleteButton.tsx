"use client";

import { deletePlaythrough } from "@/lib/mocks/mock";

export default function PlaythroughDeleteButton({ id }: { id: string }) {
  async function handleDelete() {
    const { status, response } = await deletePlaythrough(id);
    console.log(status, response.message);
  }

  return (
    <button
      onClick={handleDelete}
      className="h-8 w-20 cursor-pointer text-base shadow-md shadow-black/75 transition hover:bg-neutral-800 active:translate-y-0.5 active:shadow-black/20"
    >
      Delete
    </button>
  );
}
