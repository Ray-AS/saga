import { startGame } from "@/lib/start";

export default function StartGameButton() {
  return (
    <form action={startGame}>
      <button
        type="submit"
        className="w-32 h-10 text-xl cursor-pointer shadow-md shadow-black/50 active:translate-y-0.5 active:shadow-zinc-900"
      >
        Start
      </button>
    </form>
  );
}
