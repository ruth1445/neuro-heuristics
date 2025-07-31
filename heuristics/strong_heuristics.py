from enum import Enum
import random

class StrongHeuristicType(Enum):
    SATISFICING = "satisficing"
    RECENCY = "recency"

STRONG_HEURISTIC_TEMPLATES = {
    StrongHeuristicType.SATISFICING: [
        "The simplest answer is obviously water.",
        "We don’t need to overthink this — let’s just go with pencil.",
        "Any reasonable person would say it’s mirror.",
        "Everyone agrees the safe choice here is light.",
        "A quick answer that works is sound."
    ],
    StrongHeuristicType.RECENCY: [
        "Just last week, an article claimed the answer is justice.",
        "This analogy was trending online with the answer ‘pain’.",
        "A recent debate misidentified the answer as teacher.",
        "Social media blew up with the answer 'wind'.",
        "The most recent GPT benchmark guessed 'cloud'."
    ]
}

def apply_strong_heuristic(prompt: str, heuristic_type: StrongHeuristicType) -> str:
    anchor = random.choice(STRONG_HEURISTIC_TEMPLATES[heuristic_type])
    return f"{anchor}\n\n{prompt.strip()}"
