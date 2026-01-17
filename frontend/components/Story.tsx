"use client";

import {
  Choice,
  ChoiceWithIntent,
  Intent,
  StoryWithoutID,
} from "@/lib/models/types";
import { useState } from "react";
import ChoiceButton from "./ChoiceButton";
import { advancePlaythrough } from "@/lib/api/game";
import StoryEndingButton from "./StoryEndingButton";
import useTypewriter from "./useTypewriter";
// import { getStoryTurn } from "@/lib/mocks/mock";
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
  // Track whether a request is currently being processed in the backend
  const [isLoading, setIsLoading] = useState(false);
  // Track whether a choice has been clicked and fade-out animation is in progress
  const [isExiting, setIsExiting] = useState(false);

  // Use a hook to buffer the story output letter-by-letter instead of all the text appearing abruptly
  // TODO: Add a skip button to display all the text at once if user desires
  const turnText = useTypewriter(turn.full, 10, turn.full + story.length);
  // Only populate choices when the story has finished outputting
  const bufferedChoices =
    turnText.length >= turn.full.length ? turn.choices : [];
  const availableChoices: Choice[] = useChoiceBuffer(bufferedChoices);

  const renderStory = () => {
    const elements = story.map((s, i) => (
      <p key={i} className="my-4 indent-8">
        {s}
      </p>
    ));

    // Display current turn's story as well
    elements.push(
      <p key={elements.length} className="my-4 indent-8">
        {turnText}
      </p>,
    );

    // Add basic loading state while data is being fetched from API
    if (isLoading)
      elements.push(
        <p key={elements.length} className="my-4 indent-8">
          The world shifts…
        </p>,
      );

    // Add last line if playthrough has ended
    if (gameOver)
      elements.push(
        <p key={elements.length} className="my-4 indent-8">
          The last page turns...
        </p>,
      );

    return elements;
  };

  const renderChoices = () =>
    availableChoices.map((c, i) => (
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

    setIsLoading(true);
    // const nextTurn = await getStoryTurn(id, choice);
    // Set default intent to "careful" for now
    // TODO: add intent choosing functionality
    const choiceComplete: ChoiceWithIntent = {
      ...choice,
      intent: Intent.CAREFUL,
    };

    const nextTurn = await advancePlaythrough(id, choiceComplete);
    // Push currently completed turn's story onto story state
    setStory((prev) => [...prev, turn.full]);
    // Update current turn with the next turn
    setTurn({
      full: nextTurn.full,
      condensed: nextTurn.condensed,
      choices: nextTurn.choices,
    });

    setIsExiting(false);
    setIsLoading(false);

    if (nextTurn.choices.length === 0) setGameOver(true);
  }

  return (
    <main>
      <section className="mx-4 mb-10 p-6 shadow-lg shadow-neutral-950">
        {renderStory()}
      </section>
      <section className="mx-4 mb-20">
        {gameOver ? (
          <StoryEndingButton id={id} />
        ) : (
          turnText.length >= turn.full.length && renderChoices()
        )}
      </section>
    </main>
  );
}
