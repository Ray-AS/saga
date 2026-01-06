import LoadGameButton from "@/components/LoadGameButton";
import StartGameButton from "@/components/StartGameButton";

export default function Home() {
  return (
    <main className="flex flex-col justify-center items-center gap-4">
      <StartGameButton />
      <LoadGameButton />
    </main>
  );
}
