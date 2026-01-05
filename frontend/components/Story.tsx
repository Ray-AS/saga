'use client'

import { Choice, StoryWithoutID } from "@/lib/types";
import { useState } from "react";
import ChoiceButton from "./ChoiceButton";
import { getStoryTurn } from "@/lib/mock";

interface StoryProps {
  id: string;
  initialStory: string[];
  initialTurn: StoryWithoutID;
}

export default function Story({ id, initialStory, initialTurn }: StoryProps) {
  const [story, setStory] = useState(initialStory);
  const [turn, setTurn] = useState(initialTurn);

  const storyElements = story.map((s, i) => <p key={i}>{s}</p>);
  const choiceElements = turn.choices.map((c, i) => (
    <ChoiceButton key={i} choice={c} handleClick={handleChoice} />
  ));

  async function handleChoice(choice: Choice) {
    const { playthroughID, success, ...currentTurn  } = await getStoryTurn(id, choice);
    setStory(prev => ([...prev, turn.full]));
    setTurn(currentTurn)
  }

  return (
    <>
      <h1>Story</h1>
      {storyElements}
      <p>{turn.full}</p>
      {choiceElements}
    </>
  );
}
