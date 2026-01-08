"use client";

import { Choice, ChoiceWithIntent, Intent, StoryWithoutID } from "@/lib/models/types";
import { useState } from "react";
import ChoiceButton from "./ChoiceButton";
import { getStoryTurn } from "@/lib/mocks/mock";
import { advancePlaythrough } from "@/lib/api/game";

interface StoryProps {
  id: string;
  initialStory: string[];
  initialTurn: StoryWithoutID;
}

export default function Story({ id, initialStory, initialTurn }: StoryProps) {
  const [story, setStory] = useState(initialStory);
  const [turn, setTurn] = useState(initialTurn);

  const storyElements = story.map((s, i) => (
    <p key={i} className="my-4 indent-8">
      {s}
    </p>
  ));
  storyElements.push(
    <p key={storyElements.length} className="my-4 indent-8">
      {turn.full}
    </p>,
  );

  const choiceElements = turn.choices.map((c, i) => (
    <ChoiceButton key={i} choice={c} handleClick={handleChoice} />
  ));

  async function handleChoice(choice: Choice) {
    // const data = await getStoryTurn(id, choice);
    const choiceComplete: ChoiceWithIntent = {
      ...choice,
      intent: Intent.CAREFUL
    }
    const data = await advancePlaythrough(id, choiceComplete);
    setStory((prev) => [...prev, turn.full]);
    setTurn({
      full: data.full,
      condensed: data.condensed,
      choices: data.choices,
    });
  }

  return (
    <main>
      <section className="mx-4 mb-10 p-6 shadow-lg shadow-neutral-950">
        {storyElements}
      </section>
      <section className="mx-4 mb-20">{choiceElements}</section>
    </main>
  );
}
