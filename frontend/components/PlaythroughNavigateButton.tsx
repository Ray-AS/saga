'use client'

import { useRouter } from "next/navigation"

export default function PlaythroughNavigateButton({ id }: { id: string }) {
  const router = useRouter();

  const resumePlaythrough = () => {
    router.push(`/game/${id}`);
  };
  
  return (
    <button onClick={resumePlaythrough}>Resume</button>
  )
}