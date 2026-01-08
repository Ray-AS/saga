"use client";

import { useRouter } from "next/navigation";
import { deletePlaythrough } from "@/lib/api/game";
// import { deletePlaythrough as deletePlaythroughMock } from "@/lib/mocks/mock";

export default function PlaythroughDeleteButton({ id }: { id: string }) {
  const router = useRouter();

  // Send delete request to backend, then refresh the route to sync in frontend
  async function handleDelete() {
    // const { status, response } = await deletePlaythroughMock(id);
    // console.log(status, response.message);
    await deletePlaythrough(id);
    router.refresh();
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
