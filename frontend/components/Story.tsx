'use client'

import { StoryWithoutID } from "@/lib/types";
import { useState } from "react";
import ChoiceButton from "./ChoiceButton";

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
    <ChoiceButton key={i} choice={c} />
  ));

  return (
    <>
      <h1>Story</h1>
      {storyElements}
      <p>{turn.full}</p>
      {choiceElements}
    </>
  );
}
