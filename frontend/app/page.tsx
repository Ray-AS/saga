import LoadGameButton from "@/components/LoadGameButton";
import StartGameButton from "@/components/StartGameButton";

export default function Home() {
  return (
    <main className="flex flex-col items-center justify-center gap-4">
      <StartGameButton />
      <LoadGameButton />
    </main>
  );
}
