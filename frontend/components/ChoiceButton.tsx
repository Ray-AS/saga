import { Choice } from "@/lib/types";

interface ChoiceProps {
  choice: Choice;
  handleClick: ({ choiceDescription, difficulty, type }: Choice) => void;
}

export default function ChoiceButton({ choice, handleClick }: ChoiceProps) {
  return (
    <button data-difficulty={choice.difficulty} data-type={choice.type} onClick={() => handleClick(choice)}>
      {choice.choiceDescription}
    </button>
  );
}
