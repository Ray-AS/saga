import LoadGameButton from "@/components/LoadGameButton";
import { startGame } from "@/lib/start";

export default function Home() {
  return (
    <main>
      <h1>Saga</h1>
      <form action={startGame}>
        <button type="submit">Start</button>
      </form>
      <LoadGameButton />
    </main>
  );
}
