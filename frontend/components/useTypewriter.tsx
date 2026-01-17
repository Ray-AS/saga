"use client"

import { useEffect, useState } from "react";

export default function useTypewriter(text: string, speed: number = 20, turnID?: string) {
  const [displayed, setDisplayed] = useState("");

  useEffect(() => {
    setDisplayed("");
    if(!text) return;
    
    let i = 0;
    const interval = setInterval(() => {
      const nextChar = text[i];
      
      if (typeof nextChar === "undefined") {
        clearInterval(interval);
        return;
      }

      setDisplayed((prev) => prev + nextChar);
      i++;
      
      if (i >= text.length) {
        clearInterval(interval);
      }
    }, speed);

    return () => clearInterval(interval);
  }, [text, speed, turnID]);

  return displayed;
}