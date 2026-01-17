"use client"

import { Choice } from "@/lib/models/types";
import { useEffect, useRef, useState } from "react";

export default function useChoiceBuffer(choices: Choice[], speed: number = 300) {
  const [displayed, setDisplayed] = useState<Choice[]>([]);
  const previousChoicesRef = useRef<Choice[]>([]);

  useEffect(() => {
    if (JSON.stringify(choices) === JSON.stringify(previousChoicesRef.current)) {
      return;
    }

    previousChoicesRef.current = choices;
    setDisplayed([]);
    if(choices.length === 0) return;
    
    let i = 0;
    const interval = setInterval(() => {
      const nextChoice = choices[i];
      
      if (typeof nextChoice === "undefined") {
        clearInterval(interval);
        return;
      }

      setDisplayed((prev) => ([...prev, nextChoice]));
      i++;
      
      if (i >= choices.length) {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [choices, speed]);

  return displayed;
}