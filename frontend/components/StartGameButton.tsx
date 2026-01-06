import { startGame } from "@/lib/start";

export default function StartGameButton() {
  return (
    <form action={startGame}>
      <button
        type="submit"
        className="h-10 w-32 cursor-pointer text-xl shadow-md shadow-black/75 transition hover:bg-neutral-800 active:translate-y-0.5 active:shadow-black/20"
      >
        Start
      </button>
    </form>
  );
}
