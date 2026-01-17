"use client";

import { Choice } from "@/lib/models/types";
import { useEffect, useRef, useState } from "react";

export default function useChoiceBuffer(
  choices: Choice[],
  speed: number = 300,
) {
  // Keep track of current choices displayed
  const [displayed, setDisplayed] = useState<Choice[]>([]);
  // Keep a stable reference to last choices displayed and avoid re-renders from this by using reference
  const previousChoicesRef = useRef<Choice[]>([]);

  useEffect(() => {
    // Check if any choices have changed
    if (
      JSON.stringify(choices) === JSON.stringify(previousChoicesRef.current)
    ) {
      return;
    }

    // Update previous choices and clear the current display
    previousChoicesRef.current = choices;
    setDisplayed([]);
    if (choices.length === 0) return;

    let i = 0;
    // Display a new choice at every provided ms (default 300 ms)
    const interval = setInterval(() => {
      const nextChoice = choices[i];

      if (typeof nextChoice === "undefined") {
        clearInterval(interval);
        return;
      }

      setDisplayed((prev) => [...prev, nextChoice]);
      i++;

      // Clear interval once all choices are output
      if (i >= choices.length) {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [choices, speed]);

  return displayed;
}
