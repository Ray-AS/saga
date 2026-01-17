"use client"

import { useEffect, useState } from "react";

export default function useTypewriter(text: string, speed: number = 20, turnID?: string) {
  // Track what text is currently displayed
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    // Remove previous text
    setDisplayed("");
    if(!text) return;
    
    let i = 0;
    // Every provided ms (default 20 ms) add a character to the display text 
    const interval = setInterval(() => {
      const nextChar = text[i];
      
      if (typeof nextChar === "undefined") {
        clearInterval(interval);
        return;
      }

      setDisplayed((prev) => prev + nextChar);
      i++;
      
      // Clear interval once the text has all been output
      if (i >= text.length) {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed, turnID]);

  return displayed;
}