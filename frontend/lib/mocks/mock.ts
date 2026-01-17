import {
  StoryAdvance,
  Difficulty,
  Stat,
  StoryStart,
  Success,
  ListPlaythroughs,
  StoryRecap,
  Choice,
} from "../models/types";

const mockStart: StoryStart = {
  playthroughID: "1",
  full: "In the realm of Aethoria, where the skies were painted with hues of crimson and gold, the village of Brindlemark lay nestled within a valley. The air was alive with the whispers of ancient magic, and the villagers lived in harmony with the land. As the sun began to set, casting a warm orange glow over the thatched roofs and the bustling town square, a sense of excitement and trepidation settled over the villagers. The annual Harvest Festival was about to commence, and with it, the traditional ceremony of the Fire Dancing. The village elder, a wise and aged woman named Elara, stood at the center of the square, her eyes closed as if in meditation. The sound of drums and flutes filled the air, and the villagers began to move in rhythm, their feet stomping out a primal beat on the earth. As the music reached its crescendo, a figure emerged from the crowd, a young woman with hair as wild as the flames that danced upon the torches. She raised her arms to the sky, and the flames seemed to respond, swirling and leaping in time with her movements. The villagers watched in awe as the Fire Dancer wove her magic, the air thick with anticipation and wonder.",
  condensed:
    "The village of Brindlemark prepares for the annual Harvest Festival, featuring the traditional Fire Dancing ceremony. The village elder, Elara, oversees the event as the villagers gather in the town square. A young woman emerges, her hair wild and untamed, and raises her arms to the sky, controlling the flames that dance upon the torches.",
  choices: [
    {
      choiceDescription:
        "Approach Aria and try to strike up a conversation, sensing a potential rivalry or alliance",
      difficulty: "medium" as Difficulty,
      type: "influence" as Stat,
    },
    {
      choiceDescription:
        "Use your surroundings to your advantage, attempting to subtly outmaneuver Aria in the dance",
      difficulty: "hard" as Difficulty,
      type: "guile" as Stat,
    },
    {
      choiceDescription:
        "Show off your physical prowess, challenging Aria to a test of strength and agility",
      difficulty: "easy" as Difficulty,
      type: "force" as Stat,
    },
    {
      choiceDescription:
        "Observe the villagers and Elara, trying to understand the underlying dynamics and motivations at play",
      difficulty: "medium" as Difficulty,
      type: "insight" as Stat,
    },
  ],
};

const mockTurn: StoryAdvance = {
  ...mockStart,
  success: "SUCCESS" as Success,
};

const mockStory: StoryRecap = {
  playthroughID: "1",
  story: [
    "In the realm of Aethoria, where the skies were painted with hues of crimson and gold, the village of Brindlemark lay nestled within a valley. The air was alive with the whispers of ancient magic, and the villagers lived in harmony with the land. As the sun began to set, casting a warm orange glow over the thatched roofs and the bustling town square, a sense of excitement and trepidation settled over the villagers. The annual Harvest Festival was about to commence, and with it, the traditional ceremony of the Fire Dancing. The village elder, a wise and aged woman named Elara, stood at the center of the square, her eyes closed as if in meditation. The sound of drums and flutes filled the air, and the villagers began to move in rhythm, their feet stomping out a primal beat on the earth. As the music reached its crescendo, a figure emerged from the crowd, a young woman with hair as wild as the flames that danced upon the torches. She raised her arms to the sky, and the flames seemed to respond, swirling and leaping in time with her movements. The villagers watched in awe as the Fire Dancer wove her magic, the air thick with anticipation and wonder.",
  ],
};

const mockPlaythroughList: ListPlaythroughs = {
  playthroughs: [
    {
      playthroughID: "1",
      act: "SETUP",
      progress: 0.5,
      canEnd: false,
      summary: "playthrough summary 1",
    },
    {
      playthroughID: "2",
      act: "ESCALATION",
      progress: 0.7,
      canEnd: false,
      summary: "playthrough summary 2",
    },
    {
      playthroughID: "3",
      act: "RESOLUTION",
      progress: 0.9,
      canEnd: true,
      summary: "playthrough summary 3",
    },
  ],
};

export async function getStoryStart() {
  await new Promise((r) => setTimeout(r, 500));
  return mockStart;
}

export async function getStoryTurn(id: string, choice: Choice) {
  await new Promise((r) => setTimeout(r, 500));
  return {
    ...mockTurn,
    full: mockTurn.full || "", 
    choices: [...mockTurn.choices],
  };;
}

export const getSavedStory = (id: string) => getStoryStart();

export async function getStoryRecap(id: string) {
  await new Promise((r) => setTimeout(r, 500));
  return mockStory;
}

export async function getPlaythroughList() {
  await new Promise((r) => setTimeout(r, 500));
  return mockPlaythroughList;
}

export async function deletePlaythrough(id: string) {
  await new Promise((r) => setTimeout(r, 500));
  return {
    status: 200,
    response: { message: `Playthrough ${id} deleted` },
  };
}
