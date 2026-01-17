"use client";

import {
  Choice,
  // ChoiceWithIntent,
  // Intent,
  StoryWithoutID,
} from "@/lib/models/types";
import { useState } from "react";
import ChoiceButton from "./ChoiceButton";
// import { advancePlaythrough } from "@/lib/api/game";
import StoryEndingButton from "./StoryEndingButton";
import useTypewriter from "./useTypewriter";
import { getStoryTurn } from "@/lib/mocks/mock";
import useChoiceBuffer from "./useChoiceBuffer";

interface StoryProps {
  id: string;
  initialStory: string[];
  initialTurn: StoryWithoutID;
}

export default function Story({ id, initialStory, initialTurn }: StoryProps) {
  // Save fetched story in state and keep story updates in state so it does not need to be fetched from api each time
  const [story, setStory] = useState(initialStory);
  const [turn, setTurn] = useState(initialTurn);
  const [gameOver, setGameOver] = useState(turn.choices.length === 0);
  const [isLoading, setIsLoading] = useState(false);
  const turnText = useTypewriter(turn.full, 10, turn.full + story.length);
  const choiceBufferOptions =
    turnText.length >= turn.full.length ? turn.choices : [];
  const availableChoices: Choice[] = useChoiceBuffer(choiceBufferOptions);

  const [displayedChoices, setDisplayedChoices] = useState<Choice[]>(
    turn.choices,
  );
  const [isExiting, setIsExiting] = useState(false);

  const storyElements = story.map((s, i) => (
    <p key={i} className="my-4 indent-8">
      {s}
    </p>
  ));

  // Display current turn's story as well
  storyElements.push(
    <p key={storyElements.length} className="my-4 indent-8">
      {turnText}
    </p>,
  );

  if (isLoading) {
    storyElements.push(
      <p key={storyElements.length} className="my-4 indent-8">
        The world shifts…
      </p>,
    );
  }

  if (gameOver) {
    storyElements.push(
      <p key={storyElements.length} className="my-4 indent-8">
        The last page turns...
      </p>,
    );
  }

  const choiceElements = availableChoices.map((c, i) => (
    <ChoiceButton
      key={i}
      choice={c}
      handleClick={handleChoice}
      disabled={turnText.length < turn.full.length || isLoading}
      exiting={isExiting}
    />
  ));

  async function handleChoice(choice: Choice) {
    setIsExiting(true);
    await new Promise((resolve) => setTimeout(resolve, 600));
    setDisplayedChoices([]);

    setIsLoading(true);
    const data = await getStoryTurn(id, choice);
    // Set default intent to "careful" for now
    // TODO: add intent choosing functionality
    // const choiceComplete: ChoiceWithIntent = {
    //   ...choice,
    //   intent: Intent.CAREFUL,
    // };
    // const data = await advancePlaythrough(id, choiceComplete);
    // Push currently completed turn's story onto story state
    setStory((prev) => [...prev, turn.full]);
    // Update current turn with the next turn
    setTurn({
      full: data.full,
      condensed: data.condensed,
      choices: data.choices,
    });

    setDisplayedChoices(data.choices);
    setIsExiting(false);
    setIsLoading(false);

    if (data.choices.length === 0) setGameOver(true);
  }

  return (
    <main>
      <section className="mx-4 mb-10 p-6 shadow-lg shadow-neutral-950">
        {storyElements}
      </section>
      {!gameOver ? (
        turnText.length >= turn.full.length && (
          <section className="mx-4 mb-20">{choiceElements}</section>
        )
      ) : (
        <section className="mx-4 mb-20">
          <StoryEndingButton id={id} />
        </section>
      )}
    </main>
  );
}
