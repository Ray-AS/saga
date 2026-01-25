import { Choice } from "@/lib/models/types";

interface ChoiceProps {
  choice: Choice;
  handleClick: ({ choiceDescription, difficulty, type }: Choice) => void;
  disabled: boolean;
  exiting: boolean;
}

export default function ChoiceButton({
  choice,
  handleClick,
  disabled,
  exiting,
}: ChoiceProps) {
  return (
    <button
      onClick={() => handleClick(choice)}
      disabled={disabled}
      // FIX ENABLED BUTTON STYLING
      className={`my-2 w-full px-5 py-3 cursor-pointer text-left text-white shadow-md shadow-black/75 transition-all duration-200 ${exiting ? "animate-fade-out" : "animate-fade-in"} hover:bg-neutral-800 hover:shadow-black/60 active:translate-y-0.5 disabled:cursor-not-allowed`}
    >
      {choice.choiceDescription}
    </button>
  );
}
