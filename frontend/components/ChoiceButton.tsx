import { Choice } from "@/lib/types"

interface ChoiceProps {
  choice: Choice
}

export default function ChoiceButton({ choice }: ChoiceProps) {
  return(
    <button data-difficulty={choice.difficulty} data-type={choice.type}>{choice.choiceDescription}</button>
  )
}