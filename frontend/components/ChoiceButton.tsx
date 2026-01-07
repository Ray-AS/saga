import { Choice } from "@/lib/models/types";

interface ChoiceProps {
  choice: Choice;
  handleClick: ({ choiceDescription, difficulty, type }: Choice) => void;
}

export default function ChoiceButton({ choice, handleClick }: ChoiceProps) {
  return (
    <button
      data-difficulty={choice.difficulty}
      data-type={choice.type}
      onClick={() => handleClick(choice)}
      className="my-2 w-full cursor-pointer px-5 py-3 text-left shadow-md shadow-black/75 transition hover:bg-neutral-800 hover:shadow-black/60 active:translate-y-0.5 active:shadow-black/20"
    >
      {choice.choiceDescription}
    </button>
  );
}
