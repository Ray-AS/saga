'use client'

import { deletePlaythrough } from "@/lib/mock"

export default function PlaythroughDeleteButton({ id }: { id: string }) {
  async function handleDelete() {
    const { status, response } = await deletePlaythrough(id);
    console.log(status, response.message);
  }
  
  return (
    <button onClick={handleDelete}>Delete</button>
  )
}